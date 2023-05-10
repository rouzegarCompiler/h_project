from app import db

class DiscountCode(db.Model):
    __tablename__ = 'discount_codes'
    id = db.Column(db.Integer(),primary_key=True)
    code = db.Column(db.String(128),nullable=False,unique=True)
    value = db.Column(db.Integer(),nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(),primary_key=True)
    tariff = db.Column(db.Integer(),nullable=False)
    profit_first = db.Column(db.Integer(),nullable=False)
    profit_second = db.Column(db.Integer(),nullable=False)
    cost = db.Column(db.Integer(),nullable=False)
    daily_drawdown = db.Column(db.Integer(),nullable=False)
    metatrader_platform = db.Column(db.Integer(),nullable=False)