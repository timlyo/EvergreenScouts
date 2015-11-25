import simplejson as json

import sys
import urllib3
import certifi
from tinydb import TinyDB, Query, where

import datetime

program_db = TinyDB("data/programs.json")
users_db = TinyDB("data/users.json")
news_db = TinyDB("data/news.json")

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


def save_program_from_form(data: dict, name: str):
	"""takes the data in the format that the form gives and saves to json"""
	print("Saving", name, "program")

	events = []
	for week in data["weeks"]:
		date = week["date"].strftime("%Y-%m-%d")
		activity = week["activity"]
		notes = week["notes"]

		events.append([date, activity, notes])

		query = Query()
		result = program_db.search(query.name == name)
		if len(result) > 0:
			program_db.update({"events": events}, query.name == name)


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
def get_latest_news(count: int = None, unit="", all=False):
	result = None
	if all:
		result = news_db.all()
	elif unit == "":
		result = news_db.search(where("state") == "published")
	else:
		result = news_db.search(where("unit") == unit & (where("state") == "published"))

	if count:
		return result[:count]
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
	elif not None:
		print("Invalid value for state", state, file=sys.stderr)

	print("Update to article", id)
	print(data)
	data["updated"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	news_db.update(data, eids=[id])


def create_new_article(unit=None) -> int:
	date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	news_db.insert({"created": date, "updated": date})
