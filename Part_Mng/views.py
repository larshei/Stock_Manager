from Stock_Manager import app, db, uploaded_tables
from werkzeug import secure_filename
from Part_Mng.form import UploadXlsForm, PackageAddForm, PartAddForm, PackageAddAlternativeNameForm
from Part_Mng.models import Package, Part, AltPackage
from flask import render_template, redirect, session, request, url_for, flash
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
from openpyxl import Workbook
from datetime import datetime
import bcrypt

@app.route('/file/upload', methods=('GET', 'POST'))
def file_upload():
    form = UploadXlsForm()
    if form.validate_on_submit():
        table = request.files['import_file']
        table.save("uploads/"+form.import_type.data+"/"+secure_filename(table.filename))

        #return redirect(url_for('part_showAll'))
    return render_template('part_mng/mng_uploadXls.html', form=form)

@app.route('/part/add', methods=('GET', 'POST'))
def part_add():
    form = PartAddForm()
    if form.validate_on_submit():
        part = Part(
            form.manufacturer.data,
            form.orderingCode.data,
            form.packageSelect.data.id
        )
        db.session.add(part)
        db.session.commit()
        return redirect(url_for('part_showById', id=part.id))
    return render_template("part_mng/part_add.html", form=form);


@app.route('/showall/part')
def part_showAll():
    parts = Part.query.order_by(Part.orderingCode.asc())
    return render_template("part_mng/part_showAll.html", parts=parts)

@app.route('/show/part/<int:id>')
def part_showById(id):
    part = Part.query.filter_by(id=id).first()
    return render_template('/part_mng/part_showId.html', part=part)

@app.route('/download/part', methods=['POST'])
def part_downloadXls():
    book = Workbook() 
    sheet = book.active # currently active worksheet (default 0)

    sheet.append(['Manufacturer','Ordering Code','Package'])
    for part in Part.query.all():
        row = [part.manufacturer, part.orderingCode, part.package.name]
        sheet.append(row)    

    datetimestr = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    sheet.title = "Parts %s" % datetimestr
    book.save("generated/Parts %s.xlsx" % datetimestr)
    return redirect(url_for('package_showAll'))


@app.route('/show/package/<int:id>', methods=('GET', 'POST'))
def package_showById(id):
    form = PackageAddAlternativeNameForm()
    if form.validate_on_submit():
        alt = AltPackage(
            form.name.data,
            id
        )
        db.session.add(alt)
        db.session.commit()
    package = Package.query.filter_by(id=id).first()
    return render_template('/part_mng/package_showId.html', package=package, form=form)

@app.route('/add/package', methods=('GET', 'POST'))
def package_add():
    form = PackageAddForm()
    if form.validate_on_submit():
        package = Package(
            form.name.data,
            form.pin_count.data,
            form.pitch.data,
            form.width.data,
            form.length.data,
            form.height.data
        )
        db.session.add(package)
        db.session.commit()
        return redirect(url_for('package_showById', id=package.id))
    return render_template("part_mng/package_add.html", form=form);

@app.route('/showall/package')
def package_showAll():
    packages = Package.query.order_by(Package.name.asc())
    count = Package.query.count()
    return render_template("part_mng/package_showAll.html", packages=packages, count=count)

@app.route('/download/package', methods=['POST'])
def package_downloadXls():
    book = Workbook() 
    sheet = book.active # currently active worksheet (default 0)

    sheet.append(['Package Name','Pin Count','width','Length','height'])

    for pack in Package.query.all():
        row = [pack.name, pack.pin_count, pack.width, pack.length, pack.height]
        for altName in pack.alt_names:
            row.append(altName.name)
        sheet.append(row)    

    datetimestr = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    sheet.title = "Packages %s" % datetimestr
    book.save("generated/Packages %s.xlsx" % datetimestr)
    return redirect(url_for('package_showAll'))