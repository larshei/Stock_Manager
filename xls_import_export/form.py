from flask_wtf import Form
from wtforms import validators, RadioField
from flask_wtf.file import FileField, FileAllowed

class FileUploadForm(Form):
    import_type = RadioField('What do you want to import?', [validators.Required()], choices=[('part','Parts'),('package','Packages'),('assembly','Assembly')])
    import_file = FileField('File to Upload',  validators=[validators.Required(), FileAllowed(['xls','xlsx'], 'Excel Table Files only! (.xls, .xlsx)')])
    