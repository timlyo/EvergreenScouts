import json
import time

from website import app, data

from flask import request, jsonify, abort
from flask_login import current_user


@app.route("/api/program", methods=["GET"])
def get_program():
	name = request.args.get("name")

	if name is not None:
		print("GET to program " + name)

		program = data.get_program(name)
		return jsonify(program=program)
	else:
		print("Getting program list")
		programs = data.get_programs()
		response = jsonify(programs=programs)
		print(response)
		return response


@app.route("/api/program", methods=["POST"])
def set_program():
	if current_user.is_authenticated:
		abort(401)

	name = request.args.get("name")

	print("POST to program " + name)
	program = json.loads(request.form["events"])
	data.save_program(program, name)

	return "ok"


@app.route("/api/images", methods=["GET"])
def get_image():
	id = request.args.get("id")
	file = request.args.get("file")
	date = request.args.get("date")
	limit = request.args.get("limit")
	# TODO location
	location = request.args.get("location")

	get_all = True if len(request.args) == 0 else False  # if no arguments

	result = data.get_images(id, file, date, limit, location, get_all)
	return jsonify({"images": result})
