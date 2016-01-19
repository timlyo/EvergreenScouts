import os

from flask import Flask
import flask_login

from website import filters

app = Flask(__name__)
app.secret_key = "temp key"  # TODO change this

# badgeList = data.get_remote_json("https://raw.githubusercontent.com/timlyo/ScoutBadges/master/badges.json")
app.jinja_env.filters["format_date"] = filters.format_date
app.jinja_env.filters["format_date_readable"] = filters.format_date_readable
app.jinja_env.filters["format_date_time"] = filters.format_date_time

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config["DATA_DIRECTORY"] = os.path.join(APP_ROOT, "data/")
app.config["IMAGE_DIRECTORY"] = os.path.join(APP_ROOT, "data/images/")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

login_manager.login_view = "/login"

if not os.path.exists(app.config["DATA_DIRECTORY"]):
	os.makedirs(app.config["DATA_DIRECTORY"])
	print("Creating", app.config["DATA_DIRECTORY"])

if not os.path.exists(app.config["IMAGE_DIRECTORY"]):
	print("Creating", app.config["IMAGE_DIRECTORY"])
	os.makedirs(app.config["IMAGE_DIRECTORY"])

print("Running in", os.getcwd())