"""Jinja 2 filters file"""

import datetime


def format_date_readable(date: datetime.datetime):
    return format_date(date, "%d %b")


def format_date_time(date: datetime.datetime):
    return format_date(date, "%d %b %y %H:%M")


def format_date(date: datetime.datetime, format_string="%c"):
    assert isinstance(date, datetime.datetime), "Date must have a datetime instance, not a {}".format(type(date))

    formatted = date.strftime(format_string)

    return formatted


def is_active(name, term):
    """ return the string "active" if name matches term
    :param name: thing to match
    :param term:
    """

    if name == term:
        return "active"


def is_active_item(name, term):
    """ same as is_active but returns "active item" if name==term and "item" if not
    :param name: thing to match
    :param term:
    """

    if name == term:
        return "active item"
    else:
        return "item"
