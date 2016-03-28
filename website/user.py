import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

from website import data


class User(flask_login.UserMixin):
	def __init__(self, user_id):
		user = data.get_user_details(user_id)
		if user is None:
			raise KeyError("No user with name {}".format(user_id))

		self.id = user_id
		self.passHash = user["pw"]

	def check_password(self, password) -> bool:
		return check_password_hash(self.passHash, password)
