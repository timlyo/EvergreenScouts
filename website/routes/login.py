from website import app
from website import login_manager

from flask import render_template, request, redirect, flash, url_for
import flask_login

from website import forms, data
from website.user import User


@app.route("/login", methods=["GET", "POST"])
def login():
	print("login")
	id = request.form["user_name"]
	password = request.form["password"]
	user = None
	try:
		user = User(id)
	except KeyError as error:
		flash("No user with that name", "warning")
		print(error)
		return redirect("/")

	if user.check_password(password):
		flask_login.login_user(user)
		print(id, "has logged in")

		next = request.args.get('next')
		return redirect(next or url_for("index"))
	else:
		print(id, "failed to log in")
		flash("Incorrect password")

	return redirect("/")
	# return render_template("login.html")


@app.route("/logout")
def logout():
	print("logout")
	flask_login.logout_user()
	return redirect("/")


@login_manager.user_loader
def load_user(user_id: str):
	user = User(user_id)

	return user


@login_manager.request_loader
def request_loader(request) -> User:
	user_id = request.form.get("id")
	password = request.form.get("pw")

	if user_id is None:
		return None

	user = User(user_id)

	if user.check_password(password):
		return user
	else:
		return None
