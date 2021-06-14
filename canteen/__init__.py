from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_admin import Admin
from canteen.config import Config
from flask_admin.contrib.sqla import ModelView
from flask_principal import Principal, RoleNeed, Permission

# creating custom admin Model view to restrict users from viewing it
class CanteenModelView(ModelView):
    def is_accessible(self):
        return True if current_user.role == 'admin' else False 

    def inaccessible_callback(self, name, **kwargs):
        flash("You do not have permission to do view that!", 'danger')
        return redirect(url_for('home'))
    


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
principal = Principal()
admin = Admin(name="canteen", template_mode="bootstrap3")
admin_permission = Permission(RoleNeed('admin'))



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    principal.init_app(app)

    from canteen.users.routes import users
    from canteen.posts.routes import posts
    from canteen.main.routes import main 
    from canteen.errors.handlers import errors
    from canteen.orders.routes import orders
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(orders)

    return app

# function for dumping all the data from the database (for development only)
def dump_all_data(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

def start_app():
    app = create_app()

    from canteen.models import User, Post, OrderForm, OrderResponse

    admin.add_view(CanteenModelView(User, db.session))
    admin.add_view(CanteenModelView(Post, db.session))
    admin.add_view(CanteenModelView(OrderForm, db.session))
    admin.add_view(CanteenModelView(OrderResponse, db.session))

    #dump_all_data(app)

    return app


