from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager

from flask_mail import Mail

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

mail = Mail(app)

login = LoginManager(app)
login.login_view = "user.login"
login.login_message = "لطفاً برای ورود به این صفحه باید وارد شوید."
login.login_message_category = "warning"

from mod_user import user
app.register_blueprint(user)

from mod_admin import admin
app.register_blueprint(admin)

import views, errors