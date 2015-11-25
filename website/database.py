import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

from website import data


class User(flask_login.UserMixin):
	def __init__(self, id):
		self.id = id
		self.passHash = data.get_user(id)["pw"]

	def check_password(self, password) -> bool:
		return check_password_hash(self.passHash, password)
