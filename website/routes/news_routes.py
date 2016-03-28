from website import app

from flask import render_template, request, flash, jsonify, abort
from flask_login import login_required, current_user

import json

from website import app, data


@app.route("/news/<id>", methods=["GET"])
def news(id):
	"""
	Get page for a news article
	:param id: id of article to display
	"""
	article = data.get_article(id)
	if not article:
		return "article not found", 404
	return render_template("article.html", article=article)


@login_required
@app.route("/news/<id>/edit", methods=["GET"])
def edit_news(id):
	"""
	Page for editing a news article
	:param id: id of article to display and edit
	"""

	article = data.get_article(id)
	return render_template("admin/edit_article.html", article=article)


################################
# NEWS API
################################

@app.route("/api/news", methods=["GET"])
def search_news():
	start = request.args.get("start")
	end = request.args.get("end")
	all = request.args.get("all") is not None
	latest = data.get_latest_news(all=all)
	return jsonify(articles=latest)


@app.route("/api/news", methods=["POST"])
def create_article():
	if current_user.is_authenticated:
		data.create_new_article()
		return "ok"
	else:
		abort(401)


@app.route("/api/news/<id>", methods=["POST"])
def update_article(id):
	if current_user.is_authenticated:
		data.update_article(id, request.form)
		return "ok"
	else:
		abort(401)


@app.route("/api/news/<article_id>", methods=["DELETE"])
def delete_article(article_id):
	if current_user.is_authenticated:
		print("Deleting article: ", article_id)

		data.delete_article(article_id)
		return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
	else:
		abort(401)


@app.route("/api/news/<article_id>", methods=["RESTORE"])
def restore_article(article_id):
	if current_user.is_authenticated:
		print("Deleting article: ", article_id)

		data.restore_article(article_id)
		return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
	else:
		abort(401)


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
