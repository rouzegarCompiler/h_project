from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps

from .email import *


def user_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 1:  # user only
            return redirect(url_for("admin.panel"))
        return func(*args, **kwargs)
    return wrapper

def no_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.role == 1:
                return redirect(url_for("admin.panel"))
            else:
                return redirect(url_for("user.panel"))
        return func(*args, **kwargs)
    return wrapper