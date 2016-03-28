from website.data.database import connect_to_db, database

programs = database.table("programs")


def get_program_list():
	connect_to_db()
	return list(programs.run())


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
