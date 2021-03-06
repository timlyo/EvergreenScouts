import jinja2
from website import app
from website.data import articles, images, programmes

from flask import render_template, request, redirect
import flask
from flask_login import login_required, current_user

from flask.ext.uploads import IMAGES, secure_filename


def is_image_file(filename: str) -> bool:
	return "." in filename and filename.rsplit(".", 1)[1] in IMAGES


@app.route("/")
@app.route("/index")
def index():
	news = data.get_sidebar_articles()
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

			images.save_image(file)
			return "ok"

	return render_template("upload.html")


@app.route("/images")
def images_page():
	return render_template("images.html")


# @app.route("/<group>/badges")
# def badges(group):
#     print(group)
#     return render_template("badges.html", group=group, badges=badgeList[group])


@app.route("/<group>")
def serve_group(group):
	tab = "about"
	news = articles.get_sidebar_articles(unit=group)
	recent_images = images.get_recent_images()
	result = None
	try:
		result = render_template("group/{}.html".format(group), group=group, news=news, tab=tab, images=recent_images)
	except jinja2.exceptions.TemplateNotFound as e:
		print("No template for group:", group)
		return "not found", 404
	return result


@app.route("/<group>/programme")
def show_program(group):
	tab = "programme"
	if group == "cubs":
		thor_calendar = programmes.get_program("Thor")
		woden_calendar = programmes.get_program("Woden")

		return render_template("program.html", group="cubs", programs=[thor_calendar, woden_calendar], tab=tab)
	if group == "scouts":
		program = programmes.get_program("Scouts")

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
	return redirect("/admin/articles")


@app.route("/admin/articles")
@login_required
def admin_articles():
	deleted = request.args.get("deleted") == "true"
	articles = None
	if deleted:
		articles = data.get_all_deleted_articles()
	else:
		articles = data.get_all_undeleted_articles()

	return render_template("admin/articles.html", articles=articles, deleted=deleted)


@app.route("/admin/programs")
@login_required
def admin_programs():
	program_list = data.get_program_list()
	news_count = data.get_article_count()

	return render_template("admin/programs.html", program_list=program_list, news_count=news_count)


@app.route("/editProgram/<name>", methods=["GET"])
@login_required
def edit_program(name):
	return render_template("admin/edit_programmme.html", name=name)
