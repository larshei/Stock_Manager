from flask_wtf import FlaskForm
from part_mng.models import Part
from wtforms import StringField, validators, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField


def get_parts():
    return Part.query.order_by(Part.ordering_code.asc())
#    return Part.query.all(Part.ordering_code.acs())

class AssemblyAddForm(FlaskForm):
    name           = StringField('Assembly Name*', [validators.required(), validators.length(min=3, max=30)])
    description    = StringField('Assembly Description', [validators.length(min=0, max=200)])
    engineerSch    = StringField('SCH Engineer*', [validators.required(), validators.length(min=2, max=200)])
    engineerPcb    = StringField('PCB Engineer*', [validators.required(), validators.length(min=2, max=200)])
    year           = IntegerField('Year*', [validators.required()])
    revision       = IntegerField('Revision*', [validators.required()])

class AssemblyAddPartForm(FlaskForm):
    part_select    = QuerySelectField('Part',       query_factory=get_parts,   get_label='ordering_code')
    quantity       = IntegerField('Quantity', [validators.required()])
