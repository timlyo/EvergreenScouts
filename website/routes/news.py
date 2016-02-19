from website import app

from flask import render_template, request, flash, jsonify
from flask_login import login_required

import json

from website import app, data


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
