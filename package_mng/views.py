from Stock_Manager import app, db
from package_mng.models import Package, AltPackage
from package_mng.form import PackageAddForm, PackageAddAlternativeNameForm
from package_mng.helpers import package_in_db_get_id_or_none
from xls_import_export.helpers import already_in_list
from flask import render_template, redirect, session, request, url_for, flash


#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   this route is used to add a new package using the PackageAddForm. If the form is not validated (
#   GET method or invalid data) then the template for adding a category is displayed. If the form was
#   validated, the database is queried to make sure the given case does not exist yet (neither Package
#   nir AltPackage database). If the package exists, the user is redirected to the page of the existing
#   package, else a new package object is created and flushed to SQLAlchemys session (no commit yet!).
#   Afterwards, the AltPackage field names are evaulated. The chagnes will not be commited to the 
#   database if the alternate package was already found ind the db (and therefore linked to some other
#   package!). Duplicate names in the alt-names field will be filtered.
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/package/add', methods=('GET', 'POST'))
def package_add():
    form = PackageAddForm()
    if form.validate_on_submit():
        package_id = package_in_db_get_id_or_none(form.name.data)   # check if the package name exists as a package or as an alternative name
        if package != None:                                         # if this package has been found then abort!
            flash("Package already exists in db!", "error")         # add an error to the flash messages
            return redirect(url_for('package_showById', id = package_id))   # send to site of existing package
        package = Package(                                          # package did not exist in database: create and add to session
            form.name.data,
            form.pin_count.data,
            form.pitch.data,
            form.width.data,
            form.length.data,
            form.height.data
        )
        db.session.add(package)                                     # add the package to the session so we can link alt names to it!
        db.session.flush()                                          # flush but dont commit yet, in case we need to undo the changes

        if form.alt_names.data != "":                               # were alternative names provided?
            alt_names_to_add_to_db = []                             # store objects we will actually add to the db (not adding duplicates here!)
            identifiers_to_add = []                                 # alt package identifiers that have been processed (so we can filter additional names/duplicates)
            identifier_str = form.alt_names.data.replace(" ","")    # trim spaces
            identifier_list = identifier_str.split(",")             # split at "," and prepare a list of names
        for identifier in identifier_list:                          # check the identifiers in the list for existing packages
            existingAltPackage = package_in_db_get_id_or_none(name=identifier) 
            if existingAltPackage != None:
                flash('\"%s\" exists already, rolling back!' % identifier, "error")
                db.session.rollback()                               # if a package was found, undo!
                return redirect(url_for('package_showById', id = existingAltPackage.parent_packet.id))
            elif already_in_list(searchfor=identifier, inlist=identifiers_to_add):
                flash('Identifier \"%s\" was found twice in import file, second instance ignored' % identifier, "warning")
            else:
                flash('\"%s\" added to database' % identifier, "success")  
                parent_package_name = sheet.cell(row=index, column=form.name.data).value
                parent_id = Package.query.filter_by(name=parent_package_name).first().id
                obj = AltPackage (
                    identifier,
                    parent_id
                )
                obj_to_add_to_db.append(obj)
        db.session.add(obj_to_add_to_db)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('package_show', id=package.id))
    return render_template("package_mng/add.html", form=form, action="new")

#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Displays the information for a specific pacakage and allows to add alternative names.
#   alternative names are checked for duplicates as well as the list given by the user. 
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/package/<int:id>', methods=('GET', 'POST'))
def package_show(id):
    form = PackageAddAlternativeNameForm()                      # set the current form
    if form.validate_on_submit():                               # is this a post and are the fields as required?
        list_of_procesesed_items    = []                        # list to store names for alt packages
        list_of_items_to_add_to_db  = []                        # list to store items to be added to db
        name_list = form.name.data.replace(" ","").split(",")   # on acse multiple alternate ids were entered, lest split the string
        
        for alt_name in name_list:
            already_exists_id = package_in_db_get_id_or_none(name=alt_name) # check if we already have a package or altpackage in the db with this name
            if already_exists_id:                               # do nothing if name is already used and print an error
                flash("Package '%s' already exists in database! (See \"%s\")" \
                        %(alt_name, url_for('package_show', id=already_exists_id)),\
                        "error")                                # display an error to the user with a link to the duplicate part
            else:
                if already_in_list(alt_name, list_of_procesesed_items):
                    flash("Found duplicate in list, ignoring second instance of %s" % alt_name, \
                          "warning")                            # warn the user about naming an instance twice
                else:
                    alt = AltPackage(
                        alt_name,
                        id
                    )                                           # all is good, lets create the altPackage object
                    list_of_procesesed_items.append(alt_name)   # store name to check for duplicates
                    db.session.add(alt)
        db.session.commit()
    package = Package.query.filter_by(id=id).first()            # get the package and refrech the page
    return render_template('/package_mng/showById.html', package=package, form=form)


#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Allows editing of a package. uses the page for adding a part and pre-populates the fields
#   with data of a given object. The chagneds are thne reflected back to the object and SQLALchemy
#   will identify the changed object and to an UPDATE fpr the db 
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/package/<int:id>/edit', methods=('GET', 'POST'))
def package_edit(id):
    package = Package.query.filter_by(id=id).first_or_404()
    form = PackageAddForm(obj=package)

    alt_name_list = []
    for alt in package.alt_names:
        alt_name_list.append(alt.name)
    alt_names_string = ", ".join(alt_name_list)
    form.alt_names.data = alt_name_list
    if form.validate_on_submit():
        form.populate_obj(package)
        db.session.flush()
        db.session.commit()
        return render_template('/package_mng/showById.html', package=package, form=form)
    return render_template("package_mng/add.html", form=form, package=package, action="edit")


#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   get a list f all packages in the db and print them on the template
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/package')
def package_showAll():
    packages = Package.query.order_by(Package.name.asc())
    count = Package.query.count()
    return render_template("package_mng/showAll.html", packages=packages, count=count)

