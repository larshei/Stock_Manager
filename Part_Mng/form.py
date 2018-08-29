from flask_wtf import Form
from wtforms import validators, StringField, DecimalField,  PasswordField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class RegisterForm(Form):
    fullname = StringField('Full Name', [validators.Required()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('New Password', [
            validators.Required(),
            validators.EqualTo('confirm', message='Passwords must match'),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('New Password', [
            validators.Required(),
            validators.Length(min=4, max=80)
        ])

def cases():
    return Case.query

class PartAddForm(Form):
    manufacturer = StringField('Manufacturer', [validators.Required(), 
                                                validators.length(max=40)])
    orderingCode = StringField('Ordering Code', [validators.Required(), 
                                                validators.length(max=40)])
    category = QuerySelectField('Case', query_factory=cases, allow_blank=True)


    # TODO add category and Case selection. Allow category/case to be added on the fly?


class CaseAddForm(Form):
    name = StringField('Case Name', [validators.Required(), 
                                     validators.length(max=20)])
    pin_count       = IntegerField('Pin Count',  [validators.Required()])
    length          = DecimalField('Length',  [validators.Required()], places=2)
    width           = DecimalField('Width', [validators.Required()])
    height          = DecimalField('Height', [validators.Required()])
    pitch           = DecimalField('Pitch', [validators.Required()])
    
    #TODO is there a type that allows e.g. "tags" or "comma seperated list"??
    # alternateNames = tagFiel('Alternate Names')