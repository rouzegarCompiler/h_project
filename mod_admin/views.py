from flask import render_template,request,redirect,flash,url_for
from flask_login import current_user,login_required,logout_user

from app import db

from . import admin
from .utils import admin_only
from .forms import TicketResponseForm,CreateDiscountCodeForm,CreateProductForm,ResponseOrderForm
from .models import DiscountCode,Product

from mod_user.models import User,Ticket,Order
from mod_user.forms import ChangeInfoForm,ChangePasswordForm


@admin.route("/panel")
@admin.route("/")
@login_required
@admin_only
def panel():
    return render_template("admin/panel.html")

@admin.route("/list_users")
@login_required
@admin_only
def list_users():
    users = User.query.filter_by(role = 0).order_by(User.id.desc()).all()
    return render_template('admin/list_users.html',users=users)

@admin.route("/change_info" , methods=["GET", "POST"])
@login_required
@admin_only
def change_info():
    form = ChangeInfoForm(obj = current_user,original_email=current_user.email,orginal_idnumber=current_user.idnumber)

    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.email = form.email.data
            current_user.idnumber = form.idnumber.data
            current_user.address = form.address.data

            db.session.commit()
            
            flash("اطلاعات با موفقیت ویرایش شد.",category='success')
            return redirect(url_for('admin.panel'))
    else:
        form.populate_obj(current_user)

    return render_template("admin/change_info.html", form=form)

@admin.route("/change_user_info/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_only
def change_user_info(user_id):
    selected_user = User.query.filter_by(id=user_id).first_or_404()
    form = ChangeInfoForm(obj = selected_user,original_email=selected_user.email,orginal_idnumber=selected_user.idnumber)

    if request.method == 'POST':
        if form.validate_on_submit():
            selected_user.email = form.email.data
            selected_user.idnumber = form.idnumber.data
            selected_user.address = form.address.data

            db.session.add(selected_user)
            db.session.commit()
            
            flash("اطلاعات با موفقیت ویرایش شد.",category='warning')
            return redirect(url_for('admin.panel'))
    else:
        form.populate_obj(selected_user)

    return render_template("admin/change_user_info.html", form=form,user = selected_user)

@admin.route("/list_tickets")
@login_required
@admin_only
def list_tickets():
    tickets = Ticket.query.order_by(Ticket.id.desc()).all()

    return render_template("admin/list_tickets.html",tickets = tickets)

@admin.route("/list_tickets/<int:user_id>")
@login_required
@admin_only
def list_user_tickets(user_id):
    user = User.query.filter_by(id = user_id).first_or_404()
    
    return render_template("admin/list_user_tickets.html",user = user)

@admin.route("/ticket/<int:ticket_id>" , methods=["GET", "POST"])
@login_required
@admin_only
def ticket_response(ticket_id):
    ticket = Ticket.query.filter_by(id = ticket_id).first_or_404()
    form = TicketResponseForm()

    if request.method == "POST": 
        if form.validate_on_submit():
            ticket.response = form.response.data
            ticket.is_modified = True
            db.session.add(ticket)
            db.session.commit()

            flash("ارسال پاسخ به تیکت با موفقیت انجام شد.",category="success")
            
            return redirect(url_for("admin.list_tickets")) # change it
    else:
        form.response.data = ticket.response

    return render_template("admin/ticket_response.html",form=form, ticket=ticket)
    

@admin.route("/manage_discount_codes", methods=["GET", "POST"])
@login_required
@admin_only
def manage_discount_codes():
    form = CreateDiscountCodeForm()

    if request.method == "POST":
        if form.validate_on_submit():
            new_code = DiscountCode(code = form.code.data, value= form.value.data)
            
            db.session.add(new_code)
            db.session.commit()

            flash("ثبت کد تخفیف با موفقیت انجام شد",category="success")
            return redirect(url_for("admin.manage_discount_codes"))

    codes = DiscountCode.query.order_by(DiscountCode.id.desc()).all()
    return render_template("admin/manage_discount_codes.html",form=form, codes=codes)

@admin.route("/remove_discount_code/<int:code_id>")
@login_required
@admin_only
def remove_discount_code(code_id):
    selected_code = DiscountCode.query.filter_by(id = code_id).first()
    if selected_code:
        db.session.delete(selected_code)
        db.session.commit()
        flash("حذف کد تخفیف با موفقیت انجام شد",category="warning")

    return redirect(url_for("admin.manage_discount_codes"))

@admin.route("/manage_products", methods=["GET", "POST"])
@login_required
@admin_only
def manage_products():
    form = CreateProductForm()
    if request.method == "POST":
        if form.validate_on_submit():
            product = Product(  tariff =  form.tariff.data,
                                profit_first = form.profit_first.data,
                                profit_second = form.profit_second.data,
                                cost = form.cost.data,
                                daily_drawdown = form.daily_drawdown.data,
                                metatrader_platform = form.metatrader_platform.data
                                )
            db.session.add(product)
            db.session.commit()
            flash("ثبت محصول با موفقیت انجام شد",category="success")
            return redirect(url_for("admin.manage_products"))
    
    products = Product.query.all()
    return render_template("admin/manage_products.html", form = form, products=products)

@admin.route("/remove_product/<int:product_id>")
@login_required
@admin_only
def remove_product(product_id):
    selected_product = Product.query.filter_by(id = product_id).first()
    if selected_product:
        db.session.delete(selected_product)
        db.session.commit()
        flash("حذف محصول با موفقیت انجام شد",category="warning")
    
    return redirect(url_for("admin.manage_products"))

@admin.route("/list_orders")
@login_required
@admin_only
def list_orders():
    order_status_choices = [
        (-1, 'عدم قبول کد ارسالی'),
        (-2, 'برنده نشدن'),
        (1, 'موفقیت آمیز')
    ]

    orders = Order.query.order_by(Order.id.desc()).all()
    form = ResponseOrderForm()
    return render_template("admin/list_orders.html", orders = orders , form=form, order_status_choices = order_status_choices)

@admin.route("/reply_order/<int:order_id>", methods = ["POST"])
@login_required
@admin_only
def reply_order(order_id):
    selected_order = Order.query.filter_by(id = order_id).first()
    username_assigned = request.form.get("username_assigned")
    password_assigned = request.form.get("password_assigned")
    status = request.form.get("status")

    if selected_order:
        selected_order.username_assigned = username_assigned
        selected_order.password_assigned = password_assigned
        selected_order.status = status

        db.session.add(selected_order)
        db.session.commit()

        flash("پاسخ به سفارش کاربر با موفقیت انجام شد.", category='success')
        return redirect(url_for("admin.list_orders"))

    
    flash("سفارش مورد نظر یافت نشد.", category='danger')
    return redirect(url_for("admin.list_orders"))

@admin.route("/list_orders/<int:user_id>")
@login_required
@admin_only
def list_user_orders(user_id):
    user = User.query.filter_by(id = user_id).first_or_404()
    order_status_choices = [
        (-1, 'عدم قبول کد ارسالی'),
        (-2, 'برنده نشدن'),
        (1, 'موفقیت آمیز')
    ]
    form = ResponseOrderForm()

    return render_template("admin/list_user_orders.html",user = user,form=form, order_status_choices=order_status_choices)


@admin.route("/logout")
@admin_only
def logout():
    logout_user()
    return redirect(url_for("home"))


@admin.route("/change_password" , methods = ["GET", "POST"])
@login_required
@admin_only
def change_password():
    form = ChangePasswordForm()

    if request.method == "POST":
        if form.validate_on_submit():
            current_user.set_password(form.new_password.data)

            db.session.commit()

            flash("پسورد شما با موفقیت تغییر یافت.", category="success")

            return redirect(url_for("admin.panel"))
        
    return render_template("admin/change_password.html", form = form)