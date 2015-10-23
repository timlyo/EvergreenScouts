import argparse

from flask import Flask, render_template

from website import data

app = Flask(__name__)
badgeList = data.get_remote_json("https://raw.githubusercontent.com/timlyo/ScoutBadges/master/badges.json")


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="debug", type=bool)
    args = parser.parse_args()

    if args.debug:
        app.debug = True

    app.run()
