from Stock_Manager import app, db
from Part_Mng.form import CaseAddForm
from Part_Mng.models import Package, Part
from flask import render_template, redirect, session, request, url_for
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
import bcrypt

@app.route('/part/add', methods=('GET', 'POST'))
def addPart():
    form = CaseAddForm()
    if form.validate_on_submit():
        return redirect(url_for(showCaseWithId(id=1)))
    return render_template("part_mng/add_part.html", form=form);

@app.route('/part/showall')
def showParts():
    return render_template("part_mng/show_all_parts.html")

@app.route('/part/show/<int:id>')
def showPartWithId(id):
    part = Part.query.filter_by(id=id).first
    return render_template('/part_mng/show_part.html', part=part)

@app.route('/case/show/<int:id>')
def showCaseWithId(id):
    package = Package.query.filter_by(id=id).first()
    return render_template('/part_mng/show_case.html', package=package)

@app.route('/case/add', methods=('GET', 'POST'))
def addCase():
    form = CaseAddForm()
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
        return redirect(url_for('showCaseWithId', id=1))
    return render_template("part_mng/add_case.html", form=form);

@app.route('/case/showall')
def showCases():
    return render_template("part_mng/show_all_cases.html")

