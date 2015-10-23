import flask_login

users = {"tim": {"pw": "password"}}


class User(flask_login.UserMixin):
    pass
