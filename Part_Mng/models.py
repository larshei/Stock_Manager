from Stock_Manager import db

class Part(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(40))
    manufacturer    = db.Column(db.String(40))
    ordering_code   = db.Column(db.String(40), unique=True)
    case_id         = db.Column(db.Integer, db.ForeignKey('package.id'))
    description     = db.Column(db.String(100))
    category   = db.Column(db.Integer, db.ForeignKey('part_category.id'))

    def __init__(self, name, manufacturer, ordering_code, case_id, description="", category=None):
        self.name           = name
        self.manufacturer   = manufacturer
        self.ordering_code   = ordering_code
        self.case_id        = case_id
        self.description    = description
        self.category       = category

    def __repr__(self):
        return '<Part: %r %r>' % (self.manufacturer, self.ordering_code) 

# class DistributorOfPart(db.Model):
#     id              = db.Column(db.Integer, primary_key=True)
#     partId          = db.Column(db.Integer, db.ForeignKey('Part.id'))
#     distributor     = db.Column(db.String(20))
#     ordering_code    = db.Column(db.String(40))
#     priceEur100     = db.Column(db.Float)
#     priceEur10k     = db.Column(db.Float)

#     part = db.relationship('Part')
    
#     def __init__ (partId, distributor, ordering_code, priceEur100, priceEur10k = 0):
#         self.partId         = partId
#         self.distributor    = distributor
#         self.ordering_code   = ordering_code
#         self.priceEur100    = priceEur100
#         self.priceEur10k   = priceEur10k
    
#     def __repr__(self):
#         return '<Distributor %r for %r>' % (self.dsitributorName, self.ordering_code)
