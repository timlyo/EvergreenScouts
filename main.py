import argparse

from website import app
from website import routes

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", dest="debug", type=bool)
	args = parser.parse_args()

	if args.debug:
		app.debug = True

	app.run(threaded=True)
