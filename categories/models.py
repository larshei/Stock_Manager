from Stock_Manager import db

class PartCategory(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(30), unique=True)
    description         = db.Column(db.String(200))
    parent_category_id  = db.Column(db.Integer, db.ForeignKey('part_category.id'))

    def __init__(self, name, description="", parent_category_id=0):
        self.name               = name
        self.description        = description
        self.parent_category_id = parent_category_id

    def __repr__(self):
        return '<Category: %s>' % self.name
