from Stock_Manager          import db
from package_mng.models     import Package, AltPackage
from part_mng.models        import Part


# ===========================================
#               U T I L I T Y
# ===========================================

def package_in_db_get_id_or_none(name):
    # check primary package database:
    package = Package.query.filter_by(name=name).first()
    if package != None:
        return package.id
    # check alternative names database:
    package = AltPackage.query.filter_by(name=name).first()
    if package != None:
        return package.parent_package_id
    # nothin found, non existant:
    return None