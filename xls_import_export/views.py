import os
from Stock_Manager import app, db
from werkzeug import secure_filename
from openpyxl import Workbook
from datetime import datetime
from part_mng.models import Part
from package_mng.models import Package, AltPackage
from xls_import_export.form import FileUploadForm
from flask import render_template, redirect, request, url_for, flash


# #############################################################################
#
#                       D O W N L O A D    D A T A 
#
# #############################################################################


# creates a workbook in memory. Writes a header line based on the column
# names of the given database_table. Then querys all items in the database
# and stores their values in the workbook. Saves file when done.
def create_download_file(database_orm_obj, prefix=""):
    book = Workbook()
    sheet = book.active # currently active worksheet (default 0)

    col_keys = database_orm_obj.__table__.columns.keys()
    sheet.append(col_keys)

    for item in database_orm_obj.query.all():
        row = []
        item=item.__dict__
        for col_key in col_keys:    # ??? iterate over columns
            row.append(item[col_key])   # ??? add table row's value for this column
        sheet.append(row)             # append all the tables row values to excel file
    datetimestr = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    sheet.title = prefix + datetimestr
    book.save("generated/%s.xlsx" % sheet.title)


@app.route('/download/part', methods=['POST'])
def part_downloadXls():
    create_download_file(database_orm_obj = Part, prefix="Part_" )
    return redirect(url_for('part_showAll'))

@app.route('/download/package', methods=['POST'])
def package_downloadXls():
    create_download_file(database_orm_obj = Package, prefix="Package_" )
    return redirect(url_for('package_showAll'))


# #############################################################################
#
#                         U P L O A D    D A T A 
#
# #############################################################################

@app.route('/file/upload', methods=('GET', 'POST'))
def file_upload():
    form = FileUploadForm()
    if form.validate_on_submit():
        table = request.files['import_file']
        table.save("uploads/"+form.import_type.data+"/"+secure_filename(table.filename))
        flash('File uploaded', 'success')

        #return redirect(url_for('part_showAll'))
    return render_template('xls_import_export/upload.html', form=form)

@app.route('/file/process/<content_type>/<filename>')
def file_process(content_type, filename):
    return render_template()