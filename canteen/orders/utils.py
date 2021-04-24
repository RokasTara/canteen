from canteen.models import OrderForm, OrderResponse
from flask_login import current_user

#checking if the meal option is not empty and adding to the list for order form
def append_options(options: list) -> list:
    checked_options = []
    for option in options:
        if option:
            checked_options.append(option)
    checked_options.append('None')
    return checked_options

# returns list of ids of users that have already responded to the order form
def users_responded(order_form: OrderForm) -> list:
    ids = []
    for response in order_form.responses:
        ids.append(response.user_id)
    return ids

# returns response to the OrderFOrm of current user if it exists
def get_user_response(order_form: OrderForm) -> OrderResponse:
    for response in order_form.responses:
        if current_user.id == response.user_id:
            return response
    return None

# this function appends choices to the wtforms SelectField list
def add_order_choices(form, order_form):
    form.monday.choices = append_options([order_form.monday1, order_form.monday2, order_form.monday3])
    form.tuesday.choices = append_options([order_form.tuesday1, order_form.tuesday2, order_form.tuesday3])
    form.wednesday.choices = append_options([order_form.wednesday1, order_form.wednesday2, order_form.wednesday3])
    form.thursday.choices = append_options([order_form.thursday1, order_form.thursday2, order_form.thursday3])
    form.friday.choices = append_options([order_form.friday1, order_form.friday2, order_form.friday3])
    return form
