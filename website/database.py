import flask_login


class User(flask_login.UserMixin):
    users = {"tim@gmail.com": {"pw": "password"}}

    def __init__(self, id):
        self.id = id
        self.password = self.users[id]["pw"]
