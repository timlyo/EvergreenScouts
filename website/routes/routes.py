from website import app

from flask import render_template, request
import flask
from flask_login import login_required
from website import app, data

from flask.ext.uploads import secure_filename, IMAGES


def is_image_file(filename: str) -> bool:
	return "." in filename and filename.rsplit(".", 1)[1] in IMAGES


@app.route("/")
@app.route("/index")
def index():
	news = reversed(data.get_latest_news(5))
	return render_template("index.html", news=news)


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

	return render_template("upload.html")


@app.route("/images")
def images():
	return render_template("images.html")


@app.route("/<group>/badges")
def badges(group):
	print(group)
	return render_template("badges.html", group=group, badges=badgeList[group])


@app.route("/<group>/program")
def show_program(group):
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
	return render_template("group/cubs.html", group="cubs", news=news)


@app.route("/scouts")
def scouts():
	news = data.get_latest_news(5, unit="scouts")
	return render_template("group/scouts.html", group="scouts", news=news)


@app.route("/beavers")
def beavers():
	news = data.get_latest_news(5, unit="beavers")
	return render_template("group/beavers.html", group="beavers", news=news)


@app.route("/explorers")
def explorers():
	news = data.get_latest_news(5, unit="explorers")
	return render_template("group/explorers.html", group="beavers", news=news)


@app.route("/network")
def network():
	news = data.get_latest_news(5, unit="network")
	return render_template("group/network.html", group="beavers", news=news)


@app.route("/admin")
@login_required
def admin():
	program_list = data.get_program_list()
	articles = reversed(data.get_latest_news(all=True))
	news_count = data.get_news_count()

	return render_template("admin/admin.html", program_list=program_list, articles=articles, news_count=news_count)


@app.route("/editProgram/<name>", methods=["GET"])
@login_required
def edit_program(name):
	return render_template("admin/editProgram.html", name=name)
