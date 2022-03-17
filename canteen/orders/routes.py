from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask.helpers import make_response
from flask_login import current_user, login_required
from canteen import db, admin_permission
from canteen.models import OrderForm, OrderResponse, User
from canteen.orders.forms import OrderFormForm, OrderFormResponse
from datetime import date, datetime, timedelta
from canteen.orders.utils import Group, append_options, generate_orderForm_name, get_multiple_order_choices_counts, users_responded, get_user_response, add_order_choices, get_order_choices_counts, next_monday, generate_orderForm_name
import pdfkit

orders = Blueprint('orders', __name__)

@orders.route('/orders/forms/new', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def new_order():
    form = OrderFormForm()
    if form.validate_on_submit():
        order = OrderForm(title=form.title.data, date_expired=form.date_expired.data, date_started=form.date_started.data, monday1=form.monday1.data, monday2=form.monday2.data, monday3=form.monday3.data, tuesday1=form.tuesday1.data, tuesday2=form.tuesday2.data, tuesday3=form.tuesday3.data, wednesday1=form.wednesday1.data, wednesday2=form.wednesday2.data, wednesday3=form.wednesday3.data, thursday1=form.thursday1.data, thursday2=form.thursday2.data, thursday3=form.thursday3.data, friday1=form.friday1.data, friday2=form.friday2.data, friday3=form.friday3.data)
        db.session.add(order)
        db.session.commit()
        flash('Your order form has been created!', 'success')
        return redirect(url_for('main.home'))
    else: 
        form.title.data = generate_orderForm_name()
        form.date_started.data = next_monday()
        form.date_expired.data = next_monday()
    return render_template("create_form.html", title="New Order Form", form=form, legend='New Order Form')

@orders.route('/orders/<int:order_form_id>/fill', methods=['GET', 'POST'])
@login_required
def fill_order(order_form_id):
    order_form = OrderForm.query.get_or_404(order_form_id)
    form = OrderFormResponse()
    if current_user.id in users_responded(order_form):
        flash('You have already placed an order for this week. Please try to update it', 'danger')
        return redirect(url_for("main.home"))
    if form.validate_on_submit():
        response = OrderResponse(monday=str(form.monday.data), tuesday=form.tuesday.data, wednesday=form.wednesday.data, thursday=form.thursday.data, friday=form.friday.data, user_id=current_user.id, form_id = order_form_id)
        db.session.add(response)
        db.session.commit()
        flash('Your order has been succesfully sent!', 'success')
        return redirect(url_for('main.home'))
    else:
        form = add_order_choices(form, order_form)
        form.monday.data = 'None'
        form.tuesday.data = 'None'
        form.wednesday.data = 'None'
        form.thursday.data = 'None'
        form.friday.data = 'None'
    return render_template('order_form.html', form=form, title="Create Order", legend='Fill', name=order_form.title)

@orders.route('/orders/view')
@login_required
def order_view():
    page = request.args.get('page', 1, type=int)
    orders = OrderForm.query.order_by(OrderForm.date_posted.desc()).paginate(per_page=3, page=page)
    return render_template("your_orders.html", orders=orders, get_user_response=get_user_response, datetime=datetime, timedelta=timedelta)

@orders.route('/orders/<int:order_id>/view')
@login_required
def single_order_view(order_id):
    order = OrderForm.query.get_or_404(order_id)
    return render_template("order.html", order=order, get_user_response=get_user_response, datetime=datetime, timedelta=timedelta)

@orders.route('/orders/<int:order_id>/update', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    order = OrderForm.query.get_or_404(order_id)
    response = get_user_response(order)
    if not response:
        return redirect(url_for("orders.fill_order"), order_id)
    form = OrderFormResponse()
    if form.validate_on_submit():
        response.monday = form.monday.data
        response.tuesday = form.tuesday.data
        response.wednesday = form.wednesday.data
        response.thursday = form.thursday.data
        response.friday = form.friday.data
        db.session.commit()
        flash('Your order has been updated!', 'success')
        return redirect(url_for('orders.single_order_view', order_id=order_id))
    elif request.method == 'GET':
        form = add_order_choices(form, order)
        form.monday.data = response.monday
        form.tuesday.data = response.tuesday
        form.wednesday.data = response.wednesday
        form.thursday.data = response.thursday
        form.friday.data = response.friday
    return render_template("order_form.html", title="Update Order", form=form, legend='Update', name=order.title)
    
@orders.route('/orders/forms/<int:form_id>/view')
@login_required
@admin_permission.require()
def single_form_view(form_id):
    order = OrderForm.query.get_or_404(form_id)
    choices = get_order_choices_counts(order)
    groups = Group.get_groups()
    return render_template("form.html", order=order, choices=choices, groups=groups, len=len, zip=zip)
@orders.route('/orders/forms/<int:form_id>/pdf')
@login_required
@admin_permission.require()
def single_form_pdf(form_id):
    options = {'enable-local-file-access': None}
    order = OrderForm.query.get_or_404(form_id)
    choices = get_order_choices_counts(order)
    groups = Group.get_groups()
    rendered = render_template("pdf.html", order=order, choices=choices, groups=groups, len=len, zip=zip)
    pdf = pdfkit.from_string(rendered, False, options=options)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
    
    return response

@orders.route('/orders/forms/view')
@login_required
@admin_permission.require()
def order_forms():
    page = request.args.get('page', 1, type=int)
    orders = OrderForm.query.order_by(OrderForm.date_posted.desc()).paginate(per_page=5, page=page)
    choices = get_multiple_order_choices_counts(orders)
    return render_template("order_forms.html", orders=orders, choices=choices, len=len, zip=zip)