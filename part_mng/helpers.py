from Stock_Manager import db
from part_mng.forms import PartAddForm
from part_mng.models import Part
from categories.helpers import create_or_get_category_id 


# ===================================
#           H E L P E R S
# ===================================

def find_part_in_db(ordering_code):
    # find the part in the database
    result_db = Part.query.filter_by(ordering_code = ordering_code).first()
    return (result_db != None)


# there are 2 inputs that allow 4 combinations on how to (not) add a category.
# dropdow menu shows existing values, textbox allows entering any new category name.
# if both values are given , the existing category from the dropdown menu is set as
# the parent category. if neiter value is given, nothing is done, return None
def create_category_from_partAdd_form(form):
    cat = None
    if form.category_select is None and form.category_add.data == "":
        # neither an existing nor a new caegory has been selected, nothing to do
        pass
    elif ((form.category_select.data is not None) and (not (form.category_add.data == "") )):
        # category selected and new category specified -> create new category with
        # category from dropdown as parent
        print "creating ", form.category_add.data, " with parent ", form.category_select.data.name
        print ""
        parent_cat_id = create_or_get_category_id(form.category_select.data.name, 0)
        cat = create_or_get_category_id(form.category_add.data, parent_cat_id)

    elif form.category_add == "":
        # a category has been selected from the dropdown menu, get the id
        cat = form.category_select.id

    else:
        # new category name has been chosen, lets check if it exists and create a new
        # category with no parent if necessary. Existing categories are not changed.
        cat = create_or_get_category_id(form.category_select.name, 0)
    
    return cat.id