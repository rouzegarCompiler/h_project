from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    idnumber = db.Column(db.String(10), unique=True, nullable=False)
    address = db.Column(db.Text(), nullable=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Integer(), default=0)

    tickets = db.relationship('Ticket', backref='user_owner', lazy=True)
    orders = db.relationship('Order', backref='user_owner', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    response = db.Column(db.Text(), default="")
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    is_modified = db.Column(db.Boolean(), default=False)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(128), nullable=False)

    price = db.Column(db.Integer(), nullable=False)

    discount_code = db.Column(db.String(128), nullable=True, default=None)
    discount_value = db.Column(db.Integer(), nullable=True, default=0)

    username_assigned = db.Column(db.String(256), nullable=True, default=None)
    password_assigned = db.Column(db.String(256), nullable=True, default=None)

    status = db.Column(db.Integer(), nullable=False, default=0)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
