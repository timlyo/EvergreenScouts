import rethinkdb

database = rethinkdb.db("evergreenScouts")


def connect_to_db():
	rethinkdb.connect("localhost", 28015).repl()
