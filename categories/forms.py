from flask_wtf import Form
from wtforms import StringField, validators

class CategoryForm(Form):
    name        = StringField('Category Name*', [validators.required(), validators.length(min=3, max=40)])
    description = StringField('Category Description', [validators.length(max=40)])