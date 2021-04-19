from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from canteen import db
from canteen.models import OrderForm, OrderResponse
from canteen.orders.forms import OrderFormForm, OrderFormResponse
from datetime import date, datetime

orders = Blueprint('orders', __name__)

@orders.route('/orders/forms/new', methods=['GET', 'POST'])
@login_required
def new_order():
    form = OrderFormForm()
    if form.validate_on_submit():
        order = OrderForm(title=form.title.data, date_expired=datetime.strptime(form.date_expired.data, "%Y-%m-%d %H:%M"), date_started=datetime.strptime(form.date_started.data, "%Y-%m-%d"), monday1=form.monday1.data, monday2=form.monday2.data, monday3=form.monday3.data, tuesday1=form.tuesday1.data, tuesday2=form.tuesday2.data, tuesday3=form.tuesday3.data, wednesday1=form.wednesday1.data, wednesday2=form.wednesday2.data, wednesday3=form.wednesday3.data, thursday1=form.thursday1.data, thursday2=form.thursday2.data, thursday3=form.thursday3.data, friday1=form.friday1.data, friday2=form.friday2.data, friday3=form.friday3.data)
        db.session.add(order)
        db.session.commit()
        flash('Your order form has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template("create_form.html", title="New Order Form", form=form, legend='New Order Form')

@orders.route('/orders/forms')
@login_required
def order_forms():
    page = request.args.get('page', 1, type=int)
    orders = OrderForm.query.order_by(OrderForm.date_posted.desc()).paginate(per_page=1, page=page)
    return render_template("order_forms.html", orders=orders)

@orders.route('/orders/<int:order_form_id>/fill', methods=['GET', 'POST'])
@login_required
def fill_order(order_form_id):
    order_form = OrderForm.query.get_or_404(order_form_id)
    form = OrderFormResponse()
    form.monday.choices = [order_form.monday1, order_form.monday2, order_form.monday3, 'None']
    form.tuesday.choices = [order_form.tuesday1, order_form.tuesday2, order_form.tuesday3, 'None']
    form.wednesday.choices = [order_form.wednesday1, order_form.wednesday2, order_form.wednesday3, 'None']
    form.thursday.choices = [order_form.thursday1, order_form.thursday2, order_form.thursday3, 'None']
    form.friday.choices = [order_form.friday1, order_form.friday2, order_form.friday3, 'None']
    return render_template('order_form.html', title=order_form.title, form=form)


