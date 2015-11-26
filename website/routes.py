from website import app

from flask import render_template, request, redirect, flash
import flask_login
from flask_login import login_required

import datetime
import json

from website import app, login_manager
from website import forms
from website import data
from website import database


@app.route("/index")
@app.route("/")
def index():
	news = reversed(data.get_latest_news(5))
	return render_template("index.html", news=news)


@app.route("/upload")
def upload():
	return render_template("upload.html")


@app.route("/<group>/badges")
def badges(group):
	print(group)
	return render_template("badges.html", group=group, badges=badgeList[group])


@app.route("/<group>/program")
def get_program(group):
	if group == "cubs":
		thor_calendar = data.get_program("Thor")
		woden_calendar = data.get_program("Woden")

		return render_template("program.html", group="cubs", programs=[thor_calendar, woden_calendar])
	if group == "scouts":
		program = data.get_program("Scouts")

		return render_template("program.html", group="scouts", programs=[program])
	else:
		return "Program not found"


@app.route("/<group>/contact")
def contact(group):
	phone_number = None
	if group == "cubs":
		phone_number = data.get_user("thor")["phone"]
	return render_template("contact.html", group=group, phone_number=phone_number)


@app.route("/news/<id>")
def news(id):
	article = data.get_article(int(id))
	return render_template("news.html", article=article)


@login_required
@app.route("/news/<id>/edit", methods=["GET", "POST"])
def edit_news(id):
	id = int(id)

	if request.method == "POST":
		if not data.get_article(id):
			print("Creating article", id)
			data.create_new_article()

		form = request.form
		data.update_article(id, body=form["content"], title=form["title"], outline=form["outline"], unit=form["unit"])
		flash("Saved changes", "success")

	creating = request.args.get("action") == "create"

	article = data.get_article(id)
	return render_template("admin/editNews.html", article=article, id=id, creating=creating)


@login_required
@app.route("/news/<id>/delete", methods=["POST"])
def delete_news(id):
	id = int(id)

	data.update_article(id, state="deleted")
	return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@login_required
@app.route("/news/<id>/restore", methods=["POST"])
def restore_news(id):
	id = int(id)

	data.update_article(id, state="editing")
	return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@login_required
@app.route("/news/<id>/publish", methods=["POST"])
def publish_news(id):
	id = int(id)

	data.update_article(id, state="published")
	return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/cubs")
def cubs():
	news = data.get_latest_news(5, unit="cubs")
	return render_template("cubs.html", group="cubs", news=news)


@app.route("/scouts")
def scouts():
	news = data.get_latest_news(5, unit="scouts")
	return render_template("scouts.html", group="scouts", news=news)


@app.route("/beavers")
def beavers():
	news = data.get_latest_news(5, unit="beavers")
	print(news)
	return render_template("beavers.html", group="beavers", news=news)


@app.route("/login", methods=["GET", "POST"])
def login():
	form = forms.LoginForm(request.form)
	if form.validate_on_submit():
		id = form["user_id"].data
		user = database.User(id)
		if user.check_password(form["password"].data):
			flask_login.login_user(user)
			print(id, "has logged in")
			return redirect("/")
		else:
			print(id, "failed to log in")
			flash("Wrong username and password combination")

	return render_template("login.html", form=form)


@app.route("/logout")
def logout():
	print("logout")
	flask_login.logout_user()
	return redirect("/")


@app.route("/admin")
@login_required
def admin():
	program_list = data.get_program_list()
	articles = reversed(data.get_latest_news(all=True))
	news_count = data.get_news_count()

	return render_template("admin/admin.html", program_list=program_list, articles=articles, news_count=news_count)


@app.route("/editProgram/<name>", methods=["POST", "GET"])
@login_required
def edit_program(name):
	print("edited", name, "program")

	program_data = data.get_program(name)

	form = forms.ProgramForm(request.form)
	if request.method == "POST":
		data.save_program_from_form(form.data, name)
		flash("Saved form changes")

	else:
		for week in program_data["events"]:
			str_date = [int(x) for x in week[0].split("-")]
			date = datetime.date(str_date[0], str_date[1], str_date[2])
			form.weeks.append_entry({"date": date, "activity": week[1], "notes": week[2]})

	return render_template("admin/editProgram.html", name=name, program_data=program_data, form=form)


@login_manager.user_loader
def load_user(user_id: str):
	try:
		data.get_user(user_id)
	except KeyError:
		return None

	current_user = database.User(user_id)
	current_user.id = user_id
	return current_user


@login_manager.request_loader
def request_loader(request) -> database.User:
	user_id = request.form.get("id")
	try:
		data.get_user(user_id)
	except KeyError:
		return None

	current_user = database.User(user_id)

	current_user.is_authenticated = database.users[user_id].check_password(request.form["pw"])

	return current_user
