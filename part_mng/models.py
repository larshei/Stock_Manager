from Stock_Manager import db

class Part(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(40))
    manufacturer    = db.Column(db.String(40))
    orderingCode    = db.Column(db.String(40), unique=True)
    case_id         = db.Column(db.Integer, db.ForeignKey('package.id'))
    description     = db.Column(db.String(100))

    def __init__(self, name, manufacturer, orderingCode, case_id, description=""):
        self.name           = name
        self.manufacturer   = manufacturer
        self.orderingCode   = orderingCode
        self.case_id        = case_id

    def __repr__(self):
        return '<Part: %r %r>' % (self.manufacturer, self.orderingCode) 


class PartCategory(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(40), unique=True)
    parent_category_id  = db.Column(db.Integer)

# class DistributorOfPart(db.Model):
#     id              = db.Column(db.Integer, primary_key=True)
#     partId          = db.Column(db.Integer, db.ForeignKey('Part.id'))
#     distributor     = db.Column(db.String(20))
#     orderingCode    = db.Column(db.String(40))
#     priceEur100     = db.Column(db.Float)
#     priceEur10k     = db.Column(db.Float)

#     part = db.relationship('Part')
    
#     def __init__ (partId, distributor, orderingCode, priceEur100, priceEur10k = 0):
#         self.partId         = partId
#         self.distributor    = distributor
#         self.orderingCode   = orderingCode
#         self.priceEur100    = priceEur100
#         self.priceEur10k   = priceEur10k
    
#     def __repr__(self):
#         return '<Distributor %r for %r>' % (self.dsitributorName, self.orderingCode)
