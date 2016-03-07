import jinja2
from website import app

from flask import render_template, request
import flask
from flask_login import login_required
from website import app, data

from flask.ext.uploads import IMAGES, secure_filename


def is_image_file(filename: str) -> bool:
	return "." in filename and filename.rsplit(".", 1)[1] in IMAGES


@app.route("/")
@app.route("/index")
def index():
	news = reversed(data.get_latest_articles(5))
	return render_template("index.html", news=news, group=None)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_image():
	print("upload")
	if request.method == "POST":
		file = request.files["file"]
		if file:
			if not is_image_file(file.filename):
				print("Error", file, " not image")
				return "Not an image", 418

			data.save_image(file)
			return "ok"

	return render_template("upload.html")


@app.route("/images")
def images():
	return render_template("images.html")


# @app.route("/<group>/badges")
# def badges(group):
# 	print(group)
# 	return render_template("badges.html", group=group, badges=badgeList[group])


@app.route("/<group>")
def serve_group(group):
	tab = "about"
	news = data.get_latest_articles(5, unit=group)
	result = None
	try:
		result = render_template("group/{}.html".format(group), group=group, news=news, tab=tab)
	except jinja2.exceptions.TemplateNotFound as e:
		print("No template for group:", group)
		return "not found", 404
	return result


@app.route("/<group>/program")
def show_program(group):
	tab = "program"
	if group == "cubs":
		thor_calendar = data.get_program("Thor")
		woden_calendar = data.get_program("Woden")

		return render_template("program.html", group="cubs", programs=[thor_calendar, woden_calendar], tab=tab)
	if group == "scouts":
		program = data.get_program("Scouts")

		return render_template("program.html", group="scouts", programs=[program])
	else:
		return "Program not found"


@app.route("/<group>/contact")
def contact(group):
	tab = "contact"
	return render_template("contact.html", group=group, tab=tab)


@app.route("/admin")
@login_required
def admin():
	program_list = data.get_program_list()
	articles = reversed(data.get_latest_articles(all=True))
	news_count = data.get_article_count()

	return render_template("admin/admin.html", program_list=program_list, articles=articles, news_count=news_count)


@app.route("/editProgram/<name>", methods=["GET"])
@login_required
def edit_program(name):
	return render_template("admin/editProgram.html", name=name)
