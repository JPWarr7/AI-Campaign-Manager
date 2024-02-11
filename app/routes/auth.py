from flask import request, session, redirect, render_template, url_for, flash
from app import app
from app.database import login_query, register_query
from app.database.register import auth_query
from app.forms import LoginForm, RegisterForm


@app.route("/")
def index():
	user_id = session.get("usr_id", None)
	if not user_id:
		return redirect("/login")
	return redirect(f"/home/{user_id}")


@app.route("/login", methods=["GET", "POST"])
def login():
	login_form = LoginForm(values=request.form)
	if request.method == "POST":
		if login_form.is_valid():
			username = login_form["username"]
			password = login_form["password"]
			valid, result = login_query(username, password)
			usr_id, = result.values()
			if valid:
				session["user"] = usr_id
				flash("Login Successful", "success")
				return redirect(url_for("home", usr_id=usr_id))
			login_form.errors.update(result)
		login_form.before_render()
	else:
		login_form.clear()
	return render_template("login.html", login_form=login_form)


@app.route("/logout", methods=["GET"])
def logout():
	session["user"] = None
	return redirect("/")


def register_validate(username, password, confirm):
	_, result = auth_query(username)  # check for account with this username
	print(result)
	if result is not None:
		return False, {"username": "This username is taken!"}
	print(confirm, password, confirm == password)
	if not confirm == password:
		return False, {"confirm": "Passwords do not match!"}
	return register_query(username, password)


@app.route("/register", methods=["GET", "POST"])
def register():
	register_form = RegisterForm(values=request.form)
	if request.method == "POST":
		username = register_form["username"]
		password = register_form["password"]
		confirm = register_form["confirm"]
		if register_form.is_valid():
			(valid, result) = register_validate(username, password, confirm)
			usr_id, = result.values()
			if valid:
				session["user"] = usr_id
				flash("Login Successful", "success")
				return redirect(url_for("create_profile", usr_id=usr_id))
			register_form.errors.update(result)
		register_form.before_render()
	else:
		register_form.clear()
	return render_template("register.html", register_form=register_form)
