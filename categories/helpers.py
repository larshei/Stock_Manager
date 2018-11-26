from Stock_Manager import db
from part_mng.models import Part
from package_mng.models import Package, AltPackage
from categories.models import PartCategory

# ===========================================
#                U T I L I T Y
# ===========================================

def create_or_get_category_id(category_name, parent_category_id = 0):
        category = PartCategory.query.filter_by(name=category_name).first()
        if category is None: 
            category = PartCategory(category_name, parent_category_id)
            db.session.add(category)
            db.session.commit()
        return category.id

