"""Jinja 2 filters file"""

import datetime

import sys


def format_date_readable(date: str):
	return format_date(date, "%d %b")


def format_date_time(date: str):
	return format_date(date, "%d %b %y %H:%M")


def format_date(date: str, format="%c"):
	try:
		date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

		formatted = date.strftime(format)

		return formatted
	except ValueError as e:
		print("failed to format date: ", e, file=sys.stderr)
		return date
