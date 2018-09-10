from Stock_Manager import app, db
from part_mng.form import PartAddForm
from part_mng.models import Part
from categories.models import PartCategory
from categories.helpers import get_or_create_category_id
from package_mng.models import Package
from flask import render_template, redirect, session, request, url_for, flash


# ===================================
#           V I E W S
# ===================================
 
@app.route('/part/add', methods=('GET', 'POST'))
def part_add():
    form = PartAddForm()
    if form.validate_on_submit():
        category_id = get_or_create_category_id(form)

        part = Part(
            form.name.data,
            form.manufacturer.data,
            form.ordering_code.data,
            form.package_select.data.id,
            form.description.data,
            category_id       )
        db.session.add(part)
        db.session.commit()
        return redirect(url_for('part_show', id=part.id))
    return render_template("part_mng/add.html", form=form);


@app.route('/part')
def part_showAll():
    parts = Part.query.order_by(Part.ordering_code.asc())
    return render_template("part_mng/showAll.html", parts=parts)

@app.route('/part/<int:id>')
def part_show(id):
    part = Part.query.get(id)
    if part is None:
        return render_template("404.html", message="The Part ID could not be found in the Database")
    return render_template('/part_mng/showById.html', part=part)

@app.route('/part/<int:id>/edit', methods=['GET','POST'])
def part_edit(id):
    part = Part.query.get(id)
    if part is None:
        return render_template("404.html", message="The Part ID could not be found in the Database")
    form = PartAddForm(obj=part)
    if form.validate_on_submit():
        form.populate_obj(part)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('part_show', id=part.id))
    return render_template('/part_mng/add.html', form=form, part=part, action="edit")


