from functools import wraps
from flask import session, render_template
from app.database import profile_query


def is_trader(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        usr_id = session.get("user")
        _, result = profile_query(usr_id)
        account_type = result["account_type"]
        if not account_type == "Trader":
            return render_template("404.html")
        return route(*args, **kwargs)
    return wrapper
