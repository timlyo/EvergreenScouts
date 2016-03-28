from website.data.database import connect_to_db, database

users = database.table("users")


def get_user_details(user_id: str) -> dict:
	if user_id is None:
		return None

	connect_to_db()
	user = users.get(user_id).run()
	return user
