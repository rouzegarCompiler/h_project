from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 0:  # admin only
            flash("اجازه استفاده از این صفحه را ندارید",
                  category="warning")
            return redirect(url_for("user.panel"))
        return func(*args, **kwargs)
    return wrapper
