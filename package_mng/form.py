from flask_wtf import Form
from wtforms import validators, StringField, DecimalField,  PasswordField, IntegerField, RadioField
from package_mng.models import Package, AltPackage


class PackageAddForm(Form):
    name = StringField('Case Name', [validators.Required(), 
                                     validators.length(max=20)])
    pin_count       = IntegerField('Pin Count',  [validators.Required()])
    length          = DecimalField('Length',  [validators.Required()], places=2)
    width           = DecimalField('Width', [validators.Required()])
    height          = DecimalField('Height', [validators.Required()])
    pitch           = DecimalField('Pitch', [validators.Required()])
    
    #TODO is there a type that allows e.g. "tags" or "comma seperated list"??
    # alternateNames = tagFiel('Alternate Names')

def get_packages():
    return Package.query

class PackageAddAlternativeNameForm(Form):
    name = StringField('Case Name', [validators.Required(), 
                                     validators.length(max=20)])