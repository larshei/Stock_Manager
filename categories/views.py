from Stock_Manager import app, db
from categories.models import PartCategory
from categories.forms import CategoryForm
from flask import render_template, redirect, session, request, url_for, flash

#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Fetches a list of all entries in the PartCategory table and
#   displays them
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/category')
def category_showAll():
    categories = PartCategory.query.order_by(PartCategory.name.asc())   # get all database antries from the PartCategory table
    category_count = PartCategory.query.count()                         # get the count as well (this is slow and may need to be removed later on)
    return render_template('categories/showAll.html', categories=categories,count=category_count) # render template

#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   renders a form to add a new part. Pressing the submit button will
#   call this functon again. The form will be evaluated if this is
#   a POST, and display error messages if some validators for input
#   fields are not satisfied. If the form data is okay, a new category
#   object is created and stored in the datbsse.
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/category/add', methods=['GET','POST'])
def category_add():
    form = CategoryForm()                                           # set the category form
    if form.validate_on_submit():                                   # check if this is post and if the form has been filled out
        category = PartCategory(                                    # .. create a new PartCategory object based on form data 
            form.name.data,
            form.description.data
        )
        db.session.add(category)                                    # add the object to SQLALchemys session
        db.session.commit()                                         # update the chagnes (will recognize a newobject and INSERT)
        return redirect(url_for('category_show', id=category.id))   # redirect to show the categories details
    return render_template('categories/add.html', form=form)        # if GET or no form validation: show page for adding component

#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#      show category by id or throw a 404 i not found in database
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/category/<int:id>')
def category_show(id):
    category = PartCategory.query.filter_by(id=id).first_or_404()   # get the first object or trhow 404 if not found
    return render_template("categories/showById.html", category=category) # render template to show category data

#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   edit Category with a given ID. Throw 404 if not found. Uses the same template as the add function and passes an 
#   additional parameter to decide what kind of heading and button are required. The form is pre-populated and the
#   changes will be transfered back to the object. SQLALchemy will recognized the changed object and UPDATE it in
#   the DB on flush(regocnize?) and commit(execute?)
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/category/<int:id>/edit', methods=['GET', 'POST'])
def category_edit(id):
    category = PartCategory.query.filter_by(id=id).first_or_404()   # get the first object or throw 404 if not found
    form = CategoryForm(obj=category)                               # set the pages form and pre-populate it
    if form.validate_on_submit():                                   # if this is a POST and the form data is okay ...
        form.populate_obj(category)                                 # .. mirror the fields data back to the object 
        db.session.flush()                                          # .. and let SQLAlchemy recognize the changed object
        db.session.commit()                                         # .. to then update the databse entry
        return redirect(url_for('category_show', id=category.id))   # .. show the page of the newly created category 
    # if the form has not been validated and/or this is not a POST then display the "add" form for editing
    return render_template("categories/add.html", form=form, category=category, action="edit") 
