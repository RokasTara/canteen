from canteen import db, login_manager
from datetime import datetime, timedelta
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class OrderForm(db.Model):
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

    def get_oderform_options(self) -> dict:
        keys = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        output = {}
        for key in keys:
            tmp = {}
            for i in range(3):
                opt = getattr(self, str(key + str(i + 1)))
                if opt:
                    tmp.update({opt: 0})
            output.update({key: tmp})
        return output
    
    # returns list of ids of users that have already responded to the order form
    def users_responded(self) -> list:
        ids = []
        for response in self.responses:
            ids.append(response.user_id)
        return ids
    
    def get_any_user_response(self, user_id: int):
        for response in self.responses:
            if user_id == response.user_id:
                return response
        return None
    
    # this function calculates the total count of options for an order form 
    def get_order_choices_counts(self) -> dict:
        choice_counts = self.get_oderform_options()
        for response in self.responses:
            for day, options in choice_counts.items():
                ordered_opt = getattr(response, day)
                for opt, value in options.items():
                    if ordered_opt == opt:
                        choice_counts[day][opt] += 1
                        break

        return choice_counts

    def __repr__(self):
        return f"OrderForm('{self.title}', 'number of responses: {len(self.responses)}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False, default="first_name")
    last_name = db.Column(db.String(120), nullable=False, default="last_name")
    school_id = db.Column(db.String(20), nullable=False, default="00a00")
    group = db.Column(db.String(20), nullable=False, default="0a")
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), default='user')
    responses = db.relationship('OrderResponse', backref="User", lazy=True)

    # generates the reset token for the user
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # verifies the reset token and returns the user which generated the token to reset the password
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_response(self, order_form: OrderForm):
        for response in order_form.responses:
            if self.id == response.user_id:
                return response
        return None
    


    #formats the user's object for printing on admin panel and when debugging
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.group}')"
    


class OrderResponse(db.Model):
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


        