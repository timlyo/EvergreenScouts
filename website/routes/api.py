from website import app, data

from flask import request, jsonify


@app.route("/api/news")
def search_news():
	start = request.args.get("start")
	end = request.args.get("end")
	all = request.args.get("all") is not None
	latest = data.get_latest_news(all=all)
	return jsonify(articles=latest)


@app.route("/api/program")
def get_program():
	name = request.args.get("name")

	print("name:" + name)

	program = data.get_program(name)
	return jsonify(program)
