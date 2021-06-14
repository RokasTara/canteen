from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from canteen import db, bcrypt, principal, admin_permission
from canteen.models import User, Post
from canteen.users.forms import (RegistrationForm, LogInForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from canteen.users.utils import save_picture, send_reset_email
from flask_principal import Identity, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed

users = Blueprint('users', __name__)

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user
    if hasattr(current_user, "role"):
        identity.provides.add(RoleNeed(current_user.role))

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass, group=form.group.data, 
                    school_id = form.school_id.data, last_name=form.last_name.data, first_name=form.first_name.data)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data} successfuly! You are now able to log in', 'success')

        return redirect(url_for('users.login'))
    return render_template("register.html", title="Register", form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            identity = Identity(user.id)
            if current_user.role == "admin":
                identity.can(admin_permission)
            identity_changed.send(current_app._get_current_object(), identity=identity)
            next_page = request.args.get('next')
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

    
@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page=page)
    return render_template("user_posts.html", posts=posts, user=user)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("email has been sent with instructions to reset your password.", 'info')
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))  
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pass
        db.session.commit()
        flash('Your password has been updated', 'success')
        return redirect(url_for('users.login'))
    return render_template("reset_token.html", title='Reset Password', form=form)