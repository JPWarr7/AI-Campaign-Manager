from functools import wraps
from flask import request, session, redirect, render_template, url_for
from app import app
from app.database import update_profile_query
from app.database.profile import profile_query
from app.forms import ProfileForm
from app.routes.utils import login_required


def profile_exists(usr_id):
    _, result = profile_query(usr_id)
    blank = list(filter(lambda x: x is None, result.values()))
    return len(blank) == 0


def profile_set(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        usr_id = session.get("user")
        if not profile_exists(usr_id):
            return redirect(url_for("create_profile", usr_id=usr_id))
        return route(*args, **kwargs)

    return wrapper


def no_profile_set(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        usr_id = session.get("user")
        if profile_exists(usr_id):
            return redirect(url_for("home", usr_id=usr_id))
        return route(*args, **kwargs)

    return wrapper


@app.route("/profile/<usr_id>/create", methods=["GET", "POST"])
@login_required
@no_profile_set
def create_profile(usr_id):
    profile_form = ProfileForm(values=request.form)
    if request.method == "POST":
        if profile_form.is_valid():
            first_name = profile_form["first_name"]
            last_name = profile_form["last_name"]
            account_type = profile_form["account_type"]
            valid, result = update_profile_query(
                usr_id, first_name, last_name, account_type)
            if valid:
                return redirect(url_for("home", usr_id=usr_id))
            profile_form.errors.update(result)
        else:
            profile_form.before_render()
    return render_template(
        "create_profile.html", usr_id=usr_id,
        profile_form=profile_form)
