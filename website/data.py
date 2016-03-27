import os
import ujson as json

import sys
import urllib3
import certifi
from tinydb import TinyDB, Query, where

from PIL import Image

import datetime
import rethinkdb
import hashlib
from werkzeug.datastructures import FileStorage

from website import app
import pprint

printer = pprint.PrettyPrinter()

database = rethinkdb.db("evergreenScouts")
articles = database.table("articles")
programs = database.table("programs")
users = database.table("users")

pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


##################
# Programs
##################


def get_program_list():
	program_list = program_db.all()
	return program_list


def get_program(name: str):
	print("Getting program named:", name)
	connect_to_db()

	result = programs.get_all(name, index="name").run()
	result = list(result)
	print(result)
	if len(result) == 0:
		# TODO none found case
		pass
	elif len(result) > 1:
		return result[0]
	else:
		return result[0]


def get_programs() -> list:
	"""Return list of all programs"""
	result = program_db.all()
	print("programs", result)
	return result


def save_program(data: dict, name: str):
	"""takes the data from a dictionary and saves to disk"""
	print("Saving", name, "program")
	print(data)
	program_db.update({"events": data}, where("name") == name)


def get_json(file: str) -> dict:
	data = json.load(open(file))
	return data


def get_remote_json(url: str) -> dict:
	response = pool.request("GET", url)
	return json.loads(response.data.decode("utf-8"))


##################
# user stuff
##################

def get_user(id: str):
	connect_to_db()
	result = list(users.get_all(id, index="id").run())
	# result = users_db.search(where("id") == id)

	if len(result) == 1:
		return result[0]
	elif len(result) == 0:
		raise KeyError("No user with id " + str(id))
	else:
		print("Error: duplicate ids", result, file=sys.stderr)
		return None


##################
# Article stuff
##################

def get_latest_articles(start: int = 0, end: int = None, unit="", all=False):
	connect_to_db()

	result = None
	if all:
		result = articles.order_by(index="created").run()
	elif unit == "":
		result = articles.get_all("published", index="state").run()
	else:
		result = articles.get_all(unit, index="unit").run()  # TODO and operation

	result = list(result)

	if end:
		return result[start:end]
	else:
		return result


def get_article_count():
	return len(news_db)


def get_article_by_title(title: str):
	connect_to_db()
	result = articles.get_all(title, index="title").run()

	try:
		article = result.next()
		return article
	except rethinkdb.net.DefaultCursorEmpty:
		return None


def get_article(article_id):
	connect_to_db()
	result = articles.get(article_id).run()
	return result


def update_article(article_id, data, body=None, title=None, outline=None, unit=None, state=None):
	print("Update to article", article_id)
	print(data)
	date = rethinkdb.now()
	connect_to_db()
	articles.get(article_id).update(data).run()
	articles.get(article_id).update({"updated": date}).run()


def create_new_article():
	connect_to_db()

	date = rethinkdb.now()
	articles.insert({
		"created": date,
		"updated": None,
		"state": "editing",
		"title": "New Article",
	}).run()


####################
# images
####################

def save_image(file: FileStorage):
	thumbnail_size = 240, 240
	directory = app.config["IMAGE_DIRECTORY"]

	# Compute hash
	file_hash = hashlib.md5(file.read()).hexdigest()
	file.seek(0)

	file_name = file_hash + ".jpg"
	file_path = os.path.join(directory, file_name)
	thumbnail_name = file_hash + "_thumb.jpg"
	thumbnail_path = os.path.join(directory, thumbnail_name)

	image = Image.open(file)
	size = image.size

	if not os.path.isfile(file_path):
		# save as jpg for size efficiency
		image.save(file_path)
		print("Saved image as", file_path)

	if not os.path.isfile(thumbnail_path):
		# create thumbnail
		image = Image.open(os.path.join(directory, file_name))
		image.thumbnail(thumbnail_size, Image.ANTIALIAS)
		image.save(os.path.join(directory, thumbnail_name))
		print("saved thumbnail as", thumbnail_path)

	store_image(file_hash, size)


def store_image(file_hash: str, size: tuple):
	""" Insert image into the database
	:param file_hash: hash of the file
	:param size: tuple of image size (x, y)
	"""

	date = datetime.datetime.now().isoformat()

	images_db.insert({
		"file": file_hash,
		"date": date,
		"size": size,
		"name": ""
	})


def get_images(id_list=None, file_list=None, date=None, limit=None, location=None, get_all=False) -> list:
	if not limit:
		limit = 50

	if get_all:
		return images_db.all()[:limit]

	images = []
	if id_list:
		for id in id_list.split(","):
			try:
				id = int(id)
			except ValueError:
				continue
			result = images_db.get(eid=id)
			if result:
				images.append(result)

	if file_list:
		for file in file_list.split(","):
			result = images_db.search(where("file") == file)
			if result:
				images.append(result)

	return images[:limit]


def connect_to_db():
	rethinkdb.connect("localhost", 28015).repl()
