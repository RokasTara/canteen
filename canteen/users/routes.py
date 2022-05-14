from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from canteen import db, bcrypt, admin_permission
from canteen.models import User
from canteen.users.forms import (RegistrationForm, LogInForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from canteen.users.utils import save_picture, send_reset_email
from flask_principal import Identity, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed

users = Blueprint('users', __name__)

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Set the identity user object for permissions
    identity.user = current_user
    if hasattr(current_user, "role"):
        identity.provides.add(RoleNeed(current_user.role))

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hash the password
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #create the new user object and add it to the database
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass, group=form.group.data, 
                    school_id = form.school_id.data, last_name=form.last_name.data, first_name=form.first_name.data)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data} successfully!', 'success')

        return redirect(url_for('users.login'))
    return render_template("register.html", title="Register", form=form)

#login page route
@users.route('/login', methods=['GET', 'POST'])
def login():
    #redirecting to home page if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #if user exists and if the password matches with the password in the database
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            #principal identity gets updated with the user object
            identity = Identity(user.id)
            if current_user.role == "admin":
                identity.can(admin_permission)
            identity_changed.send(current_app._get_current_object(), identity=identity)
            next_page = request.args.get('next')
            #redirecting to the page that the user was trying to access before logging in or to the home page
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Wrong email or password. Please try again", 'danger')        
    return render_template("login.html", title="LogIn", form=form)

@users.route('/logout')
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('main.home'))
    

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account data has been updated!", 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #sending the user an email with a link to reset their password (token)
        send_reset_email(user)
        flash("email has been sent with instructions to reset your password.", 'info')
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    #verifying the token and getting the user object
    user = User.verify_reset_token(token)
    # if the token is invalid or has expired, redirect to the reset request page
    if user is None:
        flash('This is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))  
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #hash the password
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #update the password in the database
        user.password = hashed_pass
        db.session.commit()
        flash('Your password has been updated', 'success')
        return redirect(url_for('users.login'))
    return render_template("reset_token.html", title='Reset Password', form=form)