from flask_wtf import Form
from wtforms import validators, StringField, DecimalField,  PasswordField, IntegerField, RadioField
from package_mng.models import Package, AltPackage


class PackageAddForm(Form):
    name = StringField('Case Name*', [validators.Required(), 
                                     validators.length(max=20)])
    pin_count       = IntegerField( 'Pin Count')
    length          = DecimalField( 'Length',    places=2)
    width           = DecimalField( 'Width',     places=2)
    height          = DecimalField( 'Height',    places=2)
    pitch           = DecimalField( 'Pitch',     places=2)
    alt_names       = StringField(  'Alternative names (comma separated list)')

def get_packages():
    return Package.query

class PackageAddAlternativeNameForm(Form):
    name = StringField('Case Name', [validators.Required(), 
                                     validators.length(max=20)])