from flask import render_template, request, flash, redirect, url_for
from werkzeug.urls import url_parse
from flask_login import login_required, current_user, login_user, logout_user

from app import db
from . import user
from .forms import LoginForm, RegisterForm, ChangeInfoForm, TicketForm,CreateOrderForm,ChangePasswordForm,ResetPasswordRequestForm, ResetPasswordForm
from .models import User, Ticket,Order
from .utils import user_only,no_login,send_email_reset_password

from mod_admin.models import Product, DiscountCode

@user.route("/register", methods=["GET", "POST"])
@no_login
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(email=form.email.data,
                        idnumber=form.idnumber.data,
                        address=form.address.data,
                        username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("حساب کاربری شما با موفقیت ساخته شد.", category='success')
            return redirect(url_for('user.login'))

    return render_template("user/register.html", form=form)


@user.route("/login", methods=["GET", "POST"])
@no_login
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user is None:
                form.username.errors.append("نام کاربری وارد شده، یافت نشد.")

            elif not user.check_password(form.password.data):
                form.password.errors.append("گذرواژه وارد شده صحیح نیست.")

            else:
                login_user(user=user, remember=form.remember_me.data)

                # change it
                next_page = request.args.get("next")
                if not next_page or url_parse(next_page).netloc != "":
                    next_page = url_for("user.panel")
                return redirect(next_page)

    return render_template("user/login.html", form=form)


@user.route("/panel")
@user.route("/")
@login_required
@user_only
def panel():
    return render_template("user/panel.html")


@user.route("logout")
@user_only
def logout():
    logout_user()
    return redirect(url_for("home"))


@user.route("/change_info", methods=["GET", "POST"])
@login_required
@user_only
def change_info():
    form = ChangeInfoForm(obj=current_user, original_email=current_user.email,
                          orginal_idnumber=current_user.idnumber)

    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.email = form.email.data
            current_user.idnumber = form.idnumber.data
            current_user.address = form.address.data
            db.session.commit()

            flash("اطلاعات با موفقیت ویرایش شد.", category='success')
            return redirect(url_for('user.panel'))
    else:
        form.populate_obj(current_user)

    return render_template("user/change_info.html", form=form)


@user.route('/create_ticket', methods=["GET", "POST"])
@login_required
@user_only
def create_ticket():
    form = TicketForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            ticket = Ticket(title=form.title.data,
                            description=form.description.data)
            current_user.tickets.append(ticket)
            db.session.commit()
            flash("نظر شما با موفقیت ثبت شد.", category='success')
            return redirect(url_for("user.panel"))
    return render_template("user/create_ticket.html", form=form)


@user.route('/history_tickets')
@login_required
@user_only
def history_tickets():
    tickets = Ticket.query.filter_by(
        user_owner=current_user).order_by(Ticket.id.desc()).all()
    return render_template("user/history_tickets.html", tickets=tickets)


@user.route("/buy_product", methods=["GET", "POST"])
@login_required
@user_only
def buy_product():
    item_selected = request.args.get('item', default=0)
    form = CreateOrderForm()

    selected_product = Product.query.filter_by(id = item_selected).first()
    if selected_product:
        if request.method == "POST":
            if form.validate_on_submit():
                order = Order(code = form.code.data, price=selected_product.cost)
                if form.discount_code.data: # validation in form happend!
                    discount_code = DiscountCode.query.filter_by(code = form.discount_code.data).first()
                    order.discount_code = discount_code.code
                    order.discount_value = discount_code.value
                
                current_user.orders.append(order)
                db.session.commit()
                flash("خرید شما انجام شد. ادمین در اسرع وقت به خرید شما پاسخ خواهد داد.", category="success")
                
                return redirect(url_for("user.panel"))
        return render_template("user/buy_product.html", form=form, product_price = selected_product.cost, item_selected = item_selected)
        
    # Product not found
    flash("آیتم مورد نظر یافت نشد.", category="danger")
    return redirect(url_for("list_products"))

@user.route("/history_orders")
@login_required
@user_only
def history_orders():
    orders = Order.query.filter_by(
        user_owner=current_user).order_by(Order.id.desc()).all()
    return render_template("user/history_orders.html", orders=orders)


@user.route("/change_password" , methods = ["GET", "POST"])
@login_required
@user_only
def change_password():
    form = ChangePasswordForm()

    if request.method == "POST":
        if form.validate_on_submit():
            current_user.set_password(form.new_password.data)

            db.session.commit()

            flash("پسورد شما با موفقیت تغییر یافت.", category="success")

            return redirect(url_for("user.panel"))
        
    return render_template("user/change_password.html", form = form)

@user.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            
            send_email_reset_password(user)
            flash("پیامی در خصوص تغییر گذرواژه به ایمیلتان ارسال شد.", category="success")

            return redirect(url_for("user.login"))
    
    return render_template("user/reset_password_request.html", form= form)

@user.route("/reset_password/<token>",methods=["GET","POST"])
@no_login
def reset_password(token):
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("home"))
    
    form = ResetPasswordForm()
    if request.method == "POST": 
        if form.validate_on_submit():
            user.set_password(form.password.data)
            db.session.commit()
            flash("گذرواژه شما با موفقیت تغییر یافت", category="success")
            return redirect(url_for("user.login"))

    return render_template("user/reset_password.html",form=form)
