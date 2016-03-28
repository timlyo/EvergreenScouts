from website import app

from flask import request


@app.route("/api/images", methods=["GET"])
def get_image():
	image_id = request.args.get("id")
	file = request.args.get("file")
	date = request.args.get("date")
	limit = request.args.get("limit")
	# TODO location
	location = request.args.get("location")

	get_all = True if len(request.args) == 0 else False  # if no arguments

	result = data.get_images(image_id, file, date, limit, location, get_all)
	return jsonify({"images": result})
