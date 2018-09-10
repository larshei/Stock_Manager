from Stock_Manager import db
from part_mng.models import Part
from package_mng.models import Package, AltPackage
from categories.models import PartCategory

# ===========================================
#                U T I L I T Y
# ===========================================

def get_or_create_category_id(form):
    category_id = None
    category_name = form.category_add.data
    if category_name == "":
        category = PartCategory.query.filter_by(id=form.category_select.data.id).first()
        if category is None:
            return None
        else:
            return category.id
    else:
        category = PartCategory(category_name, 0)
        db.session.add(category)
        db.session.commit()
        return category.id