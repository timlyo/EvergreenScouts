"""Jinja 2 filters file"""

import datetime


def format_date(date: str):
	int_date = [int(x) for x in date.split("-")]
	date = datetime.date(int_date[0], int_date[1], int_date[2])

	formatted = date.strftime("%d %B")

	return formatted

