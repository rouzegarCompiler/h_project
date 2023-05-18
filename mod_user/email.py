from threading import Thread
from flask import render_template
from flask_mail import Message

from app import app,mail

from .TokenType import Token

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except:
            print("Email Server Error!")
            pass

def send_email(subject, sender, recipients, html_body):
    msg = Message(subject=subject, recipients=recipients, html=html_body,sender=sender)
    Thread(target=send_async_email,args=(app,msg)).start()

def send_email_reset_password(user):
    token = user.generate_token(token_type = Token.ResetPassword.value)
    subject = "بازکرداندن رمز عبور"
    sender = app.config.get("ADMIN_MAIL","info@sample.com")
    recipients = [user.email]
    html_body = render_template("user/email/_reset_password.html",user=user, token=token)
    
    send_email(subject=subject, sender=sender, recipients=recipients,html_body=html_body)
