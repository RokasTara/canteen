from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            #if the user is an admin, redirect to order form view
            return redirect(url_for('orders.order_forms'))
        if current_user.role == 'user':
            #if the user is a user (student), redirect to order view
            return redirect(url_for('orders.order_view'))    
    #if the user is not authenticated, then redirect to the login page
    return redirect(url_for("users.login"))

@main.route('/about')
def about():
    return render_template("about.html")