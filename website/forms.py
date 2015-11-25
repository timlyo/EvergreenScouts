from flask_wtf import Form
from wtforms import StringField, PasswordField, FieldList, FormField, Field
from wtforms.fields.html5 import DateField


class LoginForm(Form):
	user_id = StringField("username")
	password = PasswordField("password")


class ProgramWeek(Form):
	""" Form for a single week of the program """
	date = DateField()
	activity = StringField()
	notes = StringField()


class ProgramForm(Form):
	weeks = FieldList(FormField(ProgramWeek))
