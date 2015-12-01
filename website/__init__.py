from flask import Flask
import flask_login

from website import filters

app = Flask(__name__)
app.secret_key = "temp key"  # TODO change this

# badgeList = data.get_remote_json("https://raw.githubusercontent.com/timlyo/ScoutBadges/master/badges.json")
app.jinja_env.filters["format_date"] = filters.format_date
app.jinja_env.filters["format_date_readable"] = filters.format_date_readable
app.jinja_env.filters["format_date_time"] = filters.format_date_time

app.config["UPLOAD_FOLDER"] = "uploads/"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

login_manager.login_view = "/login"