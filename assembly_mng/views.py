from Stock_Manager import app, db
from part_mng.models import Part
from assembly_mng.models import Assembly, AssemblyParts
from assembly_mng.forms import AssemblyAddForm, AssemblyAddPartForm
from flask import render_template, redirect, session, request, url_for, flash
 


@app.route('/assembly')
def assembly_showAll():
    assemblies=Assembly.query.order_by(Assembly.name.asc())
    count=assemblies.count
    return render_template('assembly_mng/showAll.html', assemblies=assemblies, count=count)

@app.route('/assembly/<int:id>', methods=['GET','POST'])
def assembly_show(id):
    assembly = Assembly.query.filter_by(id=id).first_or_404()
    form = AssemblyAddPartForm()
    if form.validate_on_submit():
        # check if this part is already in the Assembly, update count if yes
        part_in_assembly = AssemblyParts.query.filter_by(part_id=form.part_select.data.id, assembly_id=assembly.id).first()
        if part_in_assembly is None:
            print "\n ASSOCIATION NOT FOUND! \n"
            part_to_add = AssemblyParts(part=form.part_select.data.id, assembly = assembly.id, quantity = form.quantity.data )
            db.session.add(part_to_add)
        else:
            print "\n ASSOCIATION FOUND id %s \n" % part_in_assembly
            part_in_assembly.quantity = form.quantity.data
            db.session.flush()
        db.session.commit()
    return render_template('assembly_mng/showById.html', assembly=assembly, form=form)

@app.route('/assembly/add', methods=['GET', 'POST'])
def assembly_add():
    form = AssemblyAddForm()
    if form.validate_on_submit():
        print "\n FORM FOR ASSEMBLY ADD VALIDATED \n"
        assembly = Assembly.query.filter_by(name=form.name.data).first()
        if assembly is None:
            assembly = Assembly(
                name=form.name.data,
                description=form.description.data,
                engineerSch=form.engineerSch.data,
                engineerPcb=form.engineerPcb.data,
                year=form.year.data,
                revision=form.revision.data
            )
            db.session.add(assembly)
            db.session.commit()
            print "\n REDIRECTING TO ASSEMBLY SHOW \n"
            return redirect(url_for('assembly_show', id=assembly.id))
    print "\n RENDERING TEMPLATE ADD \n"
    return render_template('assembly_mng/add.html', form=form)

@app.route('/assembly/<int:id>/edit', methods=['GET','POST'])
def assembly_edit(id):
    assembly = Assembly.query.filter_by(id=id).first_or_404()
    form = AssemblyAddForm(obj=assembly)
    if form.validate_on_submit():
        form.populate_obj(assembly)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('assembly_show', id=assembly.id))
    return render_template('assembly_mng/add.html', form=form, assembly=assembly, action="edit")
