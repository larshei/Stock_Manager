from flask_wtf import Form
from wtforms import validators, RadioField, FieldList, SelectField
from flask_wtf.file import FileField, FileAllowed

class FileUploadForm(Form):
    import_type = RadioField('What do you want to import?', [validators.Required()], choices=[('part','Parts'),('package','Packages'),('assembly','Assembly')])
    import_file = FileField('File to Upload',  validators=[validators.Required(), FileAllowed(['xls','xlsx'], 'Excel Table Files only! (.xls, .xlsx)')])


class MapTableColumnsForPartForm(Form):
    # force int as the type, so we can use the index of the element as a valid selection for "value"
    manufacturer= SelectField('Manufacturer',[validators.Required()], coerce=int)
    order_code  = SelectField('Manufacturer Ordering Code',[validators.Required()], coerce=int)
    part_name   = SelectField('Part Name',[validators.Required()], coerce=int)
    package     = SelectField('Package',[validators.Required()], coerce=int)

class MapTableColumnsForPackageForm(Form):
    # force int as the type, so we can use the index of the element as a valid selection for "value"
    name        = SelectField('Package Name',[validators.Required()], coerce=int)
    pin_count   = SelectField('Pin Count',[validators.Required()], coerce=int)
    pitch       = SelectField('Pitch',[validators.Required()], coerce=int)
    width       = SelectField('Width',[validators.Required()], coerce=int)
    length      = SelectField('Length',[validators.Required()], coerce=int)
    height      = SelectField('Height',[validators.Required()], coerce=int)
    alt_package = SelectField('Alternate Package names',[validators.Required()], coerce=int)

