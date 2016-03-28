from website.data.database import connect_to_db, database
import rethinkdb

articles = database.table("articles")


def get_sidebar_articles(unit=None) -> list:
	connect_to_db()
	query = articles.get_all([True, False], index="state")

	if unit is not None:
		query = query.filter({"unit": unit})

	return list(query.run())


def get_all_undeleted_articles() -> list:
	connect_to_db()
	query = articles.get_all(False, index="deleted")

	return list(query.run())


def get_all_deleted_articles() -> list:
	connect_to_db()
	query = articles.get_all(True, index="deleted")

	return list(query.run())


def get_latest_articles(start: int = 0, end: int = None, unit="", all=False):
	connect_to_db()

	result = None
	if all:
		result = articles.order_by(index="created").run()
	elif unit == "":
		result = articles.get_all(True, index="published").run()
	else:
		result = articles.get_all(unit, index="unit").run()  # TODO and operation

	result = list(result)

	if end:
		return result[start:end]
	else:
		return result


def get_article_count():
	return articles.count().run()


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


def update_article(article_id, data):
	print("Update to article", article_id)
	print(data)
	date = rethinkdb.now()
	connect_to_db()
	articles.get(article_id).update(data).run()
	articles.get(article_id).update({"updated": date}).run()


def delete_article(article_id):
	connect_to_db()
	articles.get(article_id).update({"deleted": True}).run()


def restore_article(article_id):
	connect_to_db()
	articles.get(article_id).update({"deleted": False}).run()


def create_new_article():
	connect_to_db()

	date = rethinkdb.now()
	articles.insert({
		"created": date,
		"updated": None,
		"published": False,
		"deleted": False,
		"title": "New Article",
	}).run()
