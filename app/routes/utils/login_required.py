from functools import wraps
from flask import redirect, url_for, session
from app.database import account_query


def login_required(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        usr_id = session.get("user")
        if usr_id is None:
            return redirect(url_for("login"))
        _, result = account_query(usr_id)
        if result is None:
            return redirect(url_for("login"))
        param = kwargs.get("usr_id", "0")
        if not usr_id == int(param):
            return redirect(url_for("logout"))
        return route(*args, **kwargs)
    return wrapper
