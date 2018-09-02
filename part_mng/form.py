from flask_wtf import Form
from wtforms import validators, StringField, DecimalField,  PasswordField, IntegerField, RadioField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from package_mng.models import Package, AltPackage

def get_packages():
    return Package.query

class PartAddForm(Form):
    manufacturer = StringField('Manufacturer', [validators.Required(), 
                                                validators.length(min=1, max=40)])
    orderingCode = StringField('Ordering Code', [validators.Required(), 
                                                validators.length(min=1, max=40)])
    name         = StringField('Part Name',     [validators.Required(), 
                                                validators.length(min=1, max=40)])
    packageSelect = QuerySelectField('Package', query_factory=get_packages, get_label='name', allow_blank=True)

    # TODO add category selection. Allow category/case to be added on the fly?
