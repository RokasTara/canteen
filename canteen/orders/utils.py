from canteen.orders.forms import OrderFormResponse
from canteen.models import OrderForm, OrderResponse, User
from flask_login import current_user
from datetime import date, timedelta
from canteen import db



#object that contains the Users from a certain group of students
class Group():
    def __init__(self, name) -> None:
        self.students = User.query.filter_by(group = name)
        self.name = name
    
    #returns a list of all distinct groups in the database    
    @staticmethod
    def get_groups() -> list: 
        groups = []
        for user in db.session.query(User.group).distinct(User.group): groups.append(Group(user.group))
        return groups
    
    #returns a dictionary of ordered number of each meal for the specific group
    def get_order_counts(self, order_form: OrderForm) -> dict:
        choice_counts = order_form.get_oderform_options()
        #iterates through all the students in the group
        for user in self.students:
            if user.get_response(order_form):
                #iterates through all days of the week
                for day, options in choice_counts.items():
                    #gets the option selected by the student for that day
                    ordered_opt = getattr(user.get_response(order_form), day)
                    #if the option is not empty, then updating the count of the option for the day of the week
                    if ordered_opt in options: 
                        choice_counts[day][ordered_opt] += 1
        return choice_counts
    


#checking if the meal option is not empty and adding to the list for order form
def append_options(options: list) -> list:
    checked_options = []
    for option in options:
        if option:
            checked_options.append(option)
    checked_options.append('None')
    return checked_options

# returns response to the OrderForm of current user if it exists
def get_user_response(order_form: OrderForm) -> OrderResponse:
    return order_form.get_any_user_response(current_user.id)


def get_multiple_order_choices_counts(orders: list) -> list:
    choices = []
    for order in orders.items: choices.append(order.get_order_choices_counts())
    return choices

# this function appends choices to the wtforms SelectField list
def add_order_choices(form, order_form) -> OrderFormResponse:
    form.monday.choices = append_options([order_form.monday1, order_form.monday2, order_form.monday3])
    form.tuesday.choices = append_options([order_form.tuesday1, order_form.tuesday2, order_form.tuesday3])
    form.wednesday.choices = append_options([order_form.wednesday1, order_form.wednesday2, order_form.wednesday3])
    form.thursday.choices = append_options([order_form.thursday1, order_form.thursday2, order_form.thursday3])
    form.friday.choices = append_options([order_form.friday1, order_form.friday2, order_form.friday3])
    return form


def next_monday() -> date: 
    days_ahead = -date.today().weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return date.today() + timedelta(days_ahead)

def generate_orderForm_name() -> str:
    start = next_monday()
    end = start + timedelta(4)
    return f"Order for {start.month:02d}/{start.day:02d} - {end.month:02d}/{end.day:02d}"
    