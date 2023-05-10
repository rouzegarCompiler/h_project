from flask_wtf import FlaskForm
from wtforms import EmailField,PasswordField,SubmitField,StringField,TextAreaField,BooleanField
from wtforms.validators import DataRequired,EqualTo,Email,Length,ValidationError

from flask_login import current_user

from .models import User

class LoginForm(FlaskForm):
    username = StringField(label="نام کاربری",validators=[DataRequired(message="وارد کردن نام کاربری الزامی است.")])
    password = PasswordField(label="گذر واژه",validators=[DataRequired(message="وارد کردن گذرواژه الزامی است.")])
    remember_me = BooleanField(label="من را به خاطر بسپار")
    submit = SubmitField(label="ورود")

class RegisterForm(FlaskForm):
    email = EmailField(label='ایمیل',validators=[DataRequired(message="تکمیل فیلد ایمیل الزامی است."),Email("فرمت ایمیل رعایت نشده است")])
    idnumber = StringField(label='کد ملی',validators=[DataRequired(message="تکمیل فیلد کد ملی الزامی است."),Length(10,10,message="کد ملی باید ده رقمی باشد.")])
    address = TextAreaField(label='آدرس')
    username = StringField(label='نام کاربری',validators=[DataRequired(message="تکمیل فیلد نام کاربری الزامی است.")])
    password = PasswordField(label='گذرواژه',validators=[DataRequired(message="تکمیل فیلد گذرواژه الزامی است.")])
    password_confirm = PasswordField(label='تایید گذرواژه',validators=[EqualTo('password',message="تایید گذرواژه با گذرواژه وارد شده یکسان نیست.")])
    submit = SubmitField(label='ثبت نام')

    def validate_email(self,email):
        user = User.query.filter(User.email.ilike(self.email.data)).first()
        if user:
            raise ValidationError("ایمیل تکراری است. لطفاً ایمیل دیگری را انتخاب کنید.")
        
    def validate_idnumber(self,idnumber):
        user = User.query.filter(User.idnumber.ilike(self.idnumber.data)).first()
        if user:
            raise ValidationError("کد ملی تکراری است. لطفاً کد ملی دیگری را انتخاب کنید.")
        
        if not idnumber.data.isnumeric():
            raise ValidationError("کد ملی باید به صورت عددی باشد.")
        
    def validate_username(self,username):
        user = User.query.filter(User.username.ilike(self.username.data)).first()
        if user:
            raise ValidationError("نام کاربری تکراری است. لطفاً نام کاربری دیگری را انتخاب کنید.")
        

class ChangeInfoForm(FlaskForm):
    email = EmailField(label='ایمیل',validators=[DataRequired(message="تکمیل فیلد ایمیل الزامی است."),Email("فرمت ایمیل رعایت نشده است")])
    idnumber = StringField(label='کد ملی',validators=[DataRequired(message="تکمیل فیلد کد ملی الزامی است."),Length(10,10,message="کد ملی باید ده رقمی باشد.")])
    address = TextAreaField(label='آدرس')
    submit = SubmitField(label='تغییر اطلاعات')

    def __init__(self, original_email ,orginal_idnumber, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = original_email
        self.original_idnumber = orginal_idnumber

    def validate_email(self,email):
        if self.original_email != email.data:
            user = User.query.filter(User.email.ilike(self.email.data)).first()
            if user :
                raise ValidationError("ایمیل تکراری است. لطفاً ایمیل دیگری را انتخاب کنید.")
        
    def validate_idnumber(self,idnumber):
        if self.original_idnumber != idnumber.data:
            user = User.query.filter(User.idnumber.ilike(self.idnumber.data)).first()
            if user:
                raise ValidationError("کد ملی تکراری است. لطفاً کد ملی دیگری را انتخاب کنید.")
        
        if not idnumber.data.isnumeric():
            raise ValidationError("کد ملی باید به صورت عددی باشد.")
        
class TicketForm(FlaskForm):
    title = StringField(label="عنوان تیکت",validators=[DataRequired(message="وارد کردن عنوان تیکت الزامی است.")])
    description = TextAreaField(label="توضیحات",validators=[DataRequired(message="وارد کردن توضیحات تیکت الزامی است.")])
    submit = SubmitField(label="ارسال")

class CreateOrderForm(FlaskForm):
    code = StringField(label="کد خرید",validators=[DataRequired(message="وارد کردن کد خرید الزامی است.")])
    discount_code = StringField(label="کد تخفیف")
    submit = SubmitField(label="خرید")

    def validate_discount_code(self,discount_code):
        from mod_admin.models import DiscountCode
        if self.discount_code.data:
            selected_discount_code = DiscountCode.query.filter(DiscountCode.code.ilike(self.discount_code.data)).first()
            if not selected_discount_code:
                raise ValidationError("کد تخفیف وارد شده یافت نشد.")
            

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(label='گذرواژه قبلی',validators=[DataRequired(message="تکمیل فیلد گذرواژه قدیمی الزامی است.")])
    new_password = PasswordField(label='گذرواژه جدید',validators=[DataRequired(message="تکمیل فیلد گذرواژه جدید الزامی است.")])
    new_password_confirm = PasswordField(label='تایید گذرواژه جدید',validators=[EqualTo('new_password',message="تایید گذرواژه جدید با گذرواژه جدید وارد شده یکسان نیست.")])
    submit = SubmitField(label='تغییر گذرواژه')

    def validate_old_password(self, old_password):
        if not current_user.check_password(old_password.data):
            raise ValidationError("پسورد قبلی به نادرستی وارد شده است.")