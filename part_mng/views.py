from Stock_Manager import app, db
from part_mng.form import PartAddForm
from part_mng.models import Part
from categories.models import PartCategory
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

# ===================================
#           H E L P E R S
# ===================================

def get_or_create_category_id(form):
    category_id = None
    category_name = form.category_add.data
    if category_name == "":
        category = PartCategory.query.filter_by(name=category_name).first()
        if category is None:
            return None
        else:
            return category.id
    else:
        category = PartCategory(category_name, 0)
        db.session.add(category)
        db.session.commit()
        return category.id