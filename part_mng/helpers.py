from Stock_Manager import db
from part_mng.models import Part

# ===================================
#           H E L P E R S
# ===================================

def find_part_in_db(ordering_code):
    # find the part in the database
    result_db = Part.query.filter_by(ordering_code = ordering_code).first()
    return (result_db != None)