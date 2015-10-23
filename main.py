import argparse

from flask import Flask, render_template
import flask_login

from flask_wtf import Form

from website import data
from website import user

app = Flask(__name__)
app.secret_key = "temp key"
badgeList = data.get_remote_json("https://raw.githubusercontent.com/timlyo/ScoutBadges/master/badges.json")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<group>/badges")
def badges(group):
    print(group)
    return render_template("badges.html", group=group, badges=badgeList[group])


@app.route("/cubs")
def cubs():
    return render_template("cubs.html", group="cubs")


@app.route("/cubs/program")
def cubs_program():
    thorCalendar = data.getJson("data/cubProgramThor.json")
    wodenCalendar = data.getJson("data/cubProgramWoden.json")

    return render_template("program.html", group="cubs", programs=[thorCalendar, wodenCalendar])


@app.route("/scouts")
def scouts():
    return render_template("scouts.html", group="scouts")


@app.route("/beavers")
def beavers():
    return render_template("beavers.html", group="beavers")

@app.route("/login")
def login():
    return render_template("login.html")


@login_manager.user_loader
def load_user(user_id):
    if user_id not in user.users:
        return None

    current_user = user.User()
    current_user.id = user_id
    return current_user


@login_manager.request_loader
def request_loader(request):
    user_id = request.form.get("id")
    if user_id not in user.users:
        return None

    current_user = User()
    current_user.id = user_id

    current_user.is_authenticated = request.form["pw"] == user.users[user_id]["pw"]

    return current_user


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="debug", type=bool)
    args = parser.parse_args()

    if args.debug:
        app.debug = True

    app.run()
