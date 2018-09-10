from flask_wtf import Form
from wtforms import validators, StringField, DecimalField,  PasswordField, IntegerField, RadioField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from package_mng.models import Package, AltPackage
from categories.models import PartCategory

def get_packages():
    return Package.query

def get_categories():
    return PartCategory.query

class PartAddForm(Form):
    manufacturer    = StringField('Manufacturer',       [validators.Required(), validators.length(min=1, max=40)])
    ordering_code   = StringField('Ordering Code',      [validators.Required(), validators.length(min=1, max=40)])
    name            = StringField('Part Name',          [validators.Required(), validators.length(min=1, max=40)])
    package_select  = QuerySelectField('Package',       query_factory=get_packages,   get_label='name', allow_blank=True)
    category_select = QuerySelectField('Part Category', query_factory=get_categories, get_label='name', allow_blank=True)
    category_add    = StringField('Add Category',       [validators.length(max=30)])
    description     = StringField('Description',        [validators.length(max=100)])


    # TODO add category selection. Allow category/case to be added on the fly?
