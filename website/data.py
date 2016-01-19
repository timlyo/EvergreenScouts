import ujson as json

import sys
import urllib3
import certifi
from tinydb import TinyDB, Query, where

import PIL

import datetime

import hashlib
from werkzeug.datastructures import FileStorage

from website import app

program_db = TinyDB(app.config["DATA_DIRECTORY"] + "/programs.json")
users_db = TinyDB(app.config["DATA_DIRECTORY"] + "/users.json")
news_db = TinyDB(app.config["DATA_DIRECTORY"] + "/news.json")
images_db = TinyDB(app.config["DATA_DIRECTORY"] + "/images.json")

pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


def get_program_list():
	program_list = program_db.all()
	return program_list


def get_program(name: str):
	program = Query()
	result = program_db.search(program["name"] == name)
	if len(result) == 1:
		return result[0]
	else:
		print(name, "program search done gone wrong:", result)
		print("len", len(result))


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


# user stuff
def get_user(id: str):
	result = users_db.search(where("id") == id)

	if len(result) == 1:
		return result[0]
	elif len(result) == 0:
		raise KeyError("No user with id " + str(id))
	else:
		print("Error: duplicate ids", result, file=sys.stderr)
		return None


# news stuff
def get_latest_news(start: int = 0, end: int = None, unit="", all=False):
	result = None
	if all:
		result = news_db.all()
	elif unit == "":
		result = news_db.search(where("state") == "published")
	else:
		result = news_db.search((where("unit") == unit) & (where("state") == "published"))

	if end:
		return result[start:end]
	else:
		return result


def get_news_count():
	return len(news_db)


def get_article(id=None):
	result = None
	if id:
		result = news_db.get(eid=id)

	return result


def update_article(id, body=None, title=None, outline=None, unit=None, state=None):
	assert isinstance(id, int), "id must be an int not a {}".format(type(id))

	data = {}
	if body:
		data["body"] = body

	if title:
		data["title"] = title

	if outline:
		data["outline"] = outline

	if unit:
		data["unit"] = unit

	if state in ["deleted", "published", "editing"]:
		data["state"] = state
	elif state is not None:
		print("Invalid value for state", state, file=sys.stderr)

	print("Update to article", id)
	print(data)
	data["updated"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	news_db.update(data, eids=[id])


def create_new_article(unit=None) -> int:
	date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	news_db.insert({"created": date, "updated": date, "state": "editing"})


# images
def save_image(image: FileStorage):
	# TODO convert to jpg
	# TODO create thumbnail
	# TODO add to database
	store_image(image)
	thumbnail


def store_image(image):
	""" Insert image into the database
	:param image: file to store
	:return:
	"""

	name = hashlib.md5(image.read()).hexdigest() + ".jpg"
	image.seek(0)
	image.save(app.config["IMAGE_DIRECTORY"] + name)

	images_db.insert({"name": name})
