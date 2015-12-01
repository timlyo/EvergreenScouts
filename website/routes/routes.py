from website import app

from flask import render_template, request, flash
import flask
from flask_login import login_required

from flaskext.uploads import secure_filename

import datetime

from website import app, forms, data


@app.route("/index")
@app.route("/")
def index():
	news = reversed(data.get_latest_news(5))
	return render_template("index.html", news=news)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
	if request.method == "POST":
		file = request.files["file"]
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path)

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
