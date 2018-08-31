from Stock_Manager import app, db
from Part_Mng.form import PackageAddForm, PartAddForm, PackageAddAlternativeNameForm
from Part_Mng.models import Package, Part, AltPackage
from flask import render_template, redirect, session, request, url_for
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
import bcrypt

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
        return redirect(url_for('part_showById', id=1))
    return render_template("part_mng/part_add.html", form=form);


@app.route('/part/showall')
def part_showAll():
    parts = Part.query.order_by(Part.orderingCode.asc())
    return render_template("part_mng/part_showAll.html", parts=parts)

@app.route('/part/show/<int:id>')
def part_showById(id):
    part = Part.query.filter_by(id=id).first()
    return render_template('/part_mng/part_showId.html', part=part)

@app.route('/package/show/<int:id>', methods=('GET', 'POST'))
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

@app.route('/package/add', methods=('GET', 'POST'))
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

@app.route('/package/showall')
def package_showAll():
    packages = Package.query.order_by(Package.name.asc())
    count = Package.query.count()
    return render_template("part_mng/package_showAll.html", packages=packages, count=count)

