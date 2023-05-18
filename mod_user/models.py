from jwt import decode as jwt_decode,encode as jwt_encode , ExpiredSignatureError, InvalidSignatureError
from datetime import datetime, timedelta,timezone
from werkzeug.security import generate_password_hash, check_password_hash

from app import app,db, login

from .TokenType import Token

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
    
    def generate_token(self,token_type):
        return jwt_encode(
            {
                "user_id": self.id,
                "type": token_type,
                "exp":datetime.now(tz=timezone.utc) + timedelta(seconds=15*60)
            },
            key = app.config.get("SECRET_KEY"),
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            decoded_token = jwt_decode(
                    jwt= token,
                    key= app.config["SECRET_KEY"],
                    algorithms=['HS256']
            )
        except (ExpiredSignatureError,InvalidSignatureError):
            return None
        
        if decoded_token.get("type") == Token.ResetPassword.value and decoded_token.get("user_id"):
            return User.query.filter_by(id = decoded_token.get("user_id")).first()
    
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
