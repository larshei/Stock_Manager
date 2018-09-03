from Stock_Manager import app, db
from part_mng.form import PartAddForm
from part_mng.models import Part
from package_mng.models import Package
from flask import render_template, redirect, session, request, url_for, flash

@app.route('/part/add', methods=('GET', 'POST'))
def part_add():
    form = PartAddForm()
    if form.validate_on_submit():
        
        part = Part(
            form.name.data,
            form.manufacturer.data,
            form.orderingCode.data,
            form.packageSelect.data.id
        )
        db.session.add(part)
        db.session.commit()
        return redirect(url_for('part_showById', id=part.id))
    return render_template("part_mng/add.html", form=form);


@app.route('/showall/part')
def part_showAll():
    parts = Part.query.order_by(Part.orderingCode.asc())
    return render_template("part_mng/showAll.html", parts=parts)

@app.route('/show/part/<int:id>')
def part_showById(id):
    part = Part.query.get(id)
    if part is None:
        return render_template("404.html", message="The Part ID could not be found in the Database")
    return render_template('/part_mng/showById.html', part=part)

    
@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")