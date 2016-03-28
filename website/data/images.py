from website.data.database import connect_to_db, database

import os

from PIL import Image

import rethinkdb
import hashlib
from werkzeug.datastructures import FileStorage

from website import app

images_table = database.table("images")


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

	connect_to_db()
	date = rethinkdb.now()

	images_table.insert({
		"file": file_hash,
		"date": date,
		"size": size,
		"name": ""
	}).run()


def get_recent_images() -> list:
	connect_to_db()
	query = images_table.order_by("date")

	return list(query.run())

