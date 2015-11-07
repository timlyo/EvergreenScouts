import flask_login
from werkzeug.security import generate_password_hash, check_password_hash


class User(flask_login.UserMixin):
	users = {
		"cubs": {"pw": "pbkdf2:sha1:1000$66Y1p9b3$2fc02f3305a5008e3e04a4e016dd9b0c67c7bd6e"}
	}

	def __init__(self, id):
		self.id = id
		self.passHash = self.users[id]["pw"]

	def check_password(self, password) -> bool:
		return check_password_hash(self.passHash, password)
