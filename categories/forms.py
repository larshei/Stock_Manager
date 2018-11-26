from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from categories.models import PartCategory

def get_categories():
    return PartCategory.query

class CategoryForm(FlaskForm):
    name        = StringField('Category Name*', [validators.required(), validators.length(min=3, max=30)])
    description = StringField('Category Description', [validators.length(max=200)])
    parent_category  = QuerySelectField('Parent Category', query_factory=get_categories, get_label='name', allow_blank=True)
#todo parent category leads to "has no parameter 'translate' when a parent category is selected on adding a new category"