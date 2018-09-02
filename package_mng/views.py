from Stock_Manager import app, db
from package_mng.models import Package, AltPackage
from package_mng.form import PackageAddForm, PackageAddAlternativeNameForm
from flask import render_template, redirect, session, request, url_for, flash


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
    return render_template('/package_mng/showById.html', package=package, form=form)

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
    return render_template("package_mng/add.html", form=form);

@app.route('/showall/package')
def package_showAll():
    packages = Package.query.order_by(Package.name.asc())
    count = Package.query.count()
    return render_template("package_mng/showAll.html", packages=packages, count=count)