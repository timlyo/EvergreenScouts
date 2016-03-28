from website import app, data

from flask import request, send_from_directory, jsonify


@app.route("/api/images", methods=["GET"])
def get_images():
	"""Get a list of image urls"""
	image_id = request.args.get("id")
	file = request.args.get("file")
	date = request.args.get("date")
	limit = request.args.get("limit")
	# TODO location
	location = request.args.get("location")

	get_all = True if len(request.args) == 0 else False  # if no arguments

	result = data.get_images(image_id, file, date, limit, location, get_all)
	return jsonify({"images": result})


@app.route("/api/images/<name>", methods=["GET"])
def get_image(name):
	"""Get a single image file"""
	return send_from_directory(app.config["IMAGE_DIRECTORY"], name)