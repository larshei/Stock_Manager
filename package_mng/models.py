from Stock_Manager import db

class Package(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(30), unique=True)
    pin_count       = db.Column(db.Integer)
    pitch           = db.Column(db.Float)
    width           = db.Column(db.Float)
    length          = db.Column(db.Float)
    height          = db.Column(db.Float)
    alt_names       = db.relationship('AltPackage', backref='package', lazy='dynamic')
    parts           = db.relationship('Part', backref='package', lazy='dynamic')

    def __init__(self, name, pin_count, pitch, width, length, height):
        self.name            = name
        self.pin_count       = pin_count
        self.pitch           = pitch
        self.width           = width
        self.length          = length
        self.height          = height

    def __repr__(self):
        return '<Package: %r>' % self.name

class AltPackage(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(20), unique=True)
    parent_package_id   = db.Column(db.Integer, db.ForeignKey('package.id'))

    def __init__(self, name, parent_id):
        self.name = name
        self.parent_package_id = parent_id
            
    def __repr__(self):
        return '<Case Alternate name: %r>' % self.name