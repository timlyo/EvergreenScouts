import argparse

from flask import Flask, render_template, request
import flask_login
from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms import PasswordField

from website import data
from website import database

app = Flask(__name__)
app.secret_key = "temp key"
badgeList = data.get_remote_json("https://raw.githubusercontent.com/timlyo/ScoutBadges/master/badges.json")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class LoginForm(Form):
    user_id = EmailField("username")
    password = PasswordField("password")


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


@flask_login.login_required
@app.route("/beavers")
def beavers():
    return render_template("beavers.html", group="beavers")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        id = form["user_id"].data
        user = database.User(id)
        if user.password == form["password"].data:
            flask_login.login_user(user)
            print(id, "has logged in")
        else:
            print(id, "failed to log in")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    print("logout")
    flask_login.logout_user()
    return "ok"


@login_manager.user_loader
def load_user(id):
    if id not in database.User.users:
        return None

    current_user = database.User(id)
    current_user.id = id
    return current_user


@login_manager.request_loader
def request_loader(request):
    user_id = request.form.get("id")
    if user_id not in database.User.users:
        return None

    current_user = database.User(user_id)

    current_user.is_authenticated = request.form["pw"] == database.users[user_id]["pw"]

    return current_user


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="debug", type=bool)
    args = parser.parse_args()

    if args.debug:
        app.debug = True

    app.run()
