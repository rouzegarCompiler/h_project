from flask_wtf import FlaskForm
from wtforms import SubmitField,TextAreaField,StringField,IntegerField,SelectField,RadioField
from wtforms.validators import DataRequired,ValidationError,NumberRange

from .models import DiscountCode

class TicketResponseForm(FlaskForm):
    response = TextAreaField(label="پاسخ",validators=[DataRequired("وارد کردن پاسخ الزامی است.")])
    submit = SubmitField(label="ارسال")

class CreateDiscountCodeForm(FlaskForm):
    code = StringField(label="کد",validators=[DataRequired("وارد کردن کد الزامی است.")])
    value = IntegerField(label="میزان تخفیف",validators=[DataRequired("وارد کردن کد الزامی است."),NumberRange(min=1,max=100,message="کد تخفیف باید عددی در بازه ی 1 تا 100 درصد باشد.")])
    submit = SubmitField(label="ثبت")

    def validate_code(self,code):
        found_code = DiscountCode.query.filter(DiscountCode.code.ilike(self.code.data)).first()
        if found_code:
            raise ValidationError("کد تخفیف تکراری است. لطفاً کد تخفیف دیگری را انتخاب کنید.")


class CreateProductForm(FlaskForm):
    tariff = IntegerField(label="تعرفه",validators=[DataRequired("وارد کردن مبلغ تعرفه الزامی است.")])
    profit_first = IntegerField(label="سود اولیه",validators=[DataRequired("وارد کردن سود مرحله اول الزامی است.")])
    profit_second = IntegerField(label="سود ثانویه",validators=[DataRequired("وارد کردن سود مرحله دوم الزامی است.")])
    cost = IntegerField(label="هزینه تعرفه",validators=[DataRequired("وارد کردن سود مرحله دوم الزامی است.")])
    daily_drawdown = IntegerField(label="کاهش سود روزانه",validators=[DataRequired("وارد کردن میزان کاهش سود روزانه الزامی است.")])
    metatrader_platform = IntegerField(label="ورژن متاتریدیر",validators=[DataRequired("وارد کردن ورژن متاتریدر الزامی است.")])
    submit = SubmitField(label="ثبت")

class ResponseOrderForm(FlaskForm):
    username_assigned = StringField(label="یوزنیم انتسابی")
    password_assigned = StringField(label="پسورد انتسابی")

    submit = SubmitField(label="ذخیره")