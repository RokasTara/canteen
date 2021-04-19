from canteen import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    responses = db.relationship('OrderResponse', backref="User", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
     

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class OrderForm(db.Model, UserMixin):
    __tablename__ = 'order_form'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_expired = db.Column(db.DateTime(), nullable=False)
    date_posted = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    date_started = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    monday1 = db.Column(db.String(100))
    monday2 = db.Column(db.String(100))
    monday3 = db.Column(db.String(100))

    tuesday1 = db.Column(db.String(100))
    tuesday2 = db.Column(db.String(100))
    tuesday3 = db.Column(db.String(100))

    wednesday1 = db.Column(db.String(100))   
    wednesday2 = db.Column(db.String(100))
    wednesday3 = db.Column(db.String(100))

    thursday1 = db.Column(db.String(100))
    thursday2 = db.Column(db.String(100))
    thursday3 = db.Column(db.String(100))

    friday1 = db.Column(db.String(100))
    friday2 = db.Column(db.String(100))
    friday3 = db.Column(db.String(100))

    responses = db.relationship('OrderResponse', backref="Order Form", lazy=True)

class OrderResponse(db.Model, UserMixin):
    __tablename__ = 'order_response'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    monday = db.Column(db.String(100))
    tuesday = db.Column(db.String(100))
    wednesday = db.Column(db.String(100))
    thursday = db.Column(db.String(100))
    friday = db.Column(db.String(100))
    form_id = db.Column(db.Integer, db.ForeignKey('order_form.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


        