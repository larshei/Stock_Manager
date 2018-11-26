from Stock_Manager import db
from part_mng.models import Part


class Assembly(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(30))
    description         = db.Column(db.String(200))
    engineerSch         = db.Column(db.String(50))
    engineerPcb         = db.Column(db.String(50))
    year                = db.Column(db.Integer)
    revision            = db.Column(db.Integer)

    parts               = db.relationship('Part', secondary='assembly_part_association', backref='assembly', lazy='dynamic')


    def __init__(self, name, engineerSch, engineerPcb, year, revision,  description=""):
        self.name        = name
        self.description = description
        self.engineerSch = engineerSch
        self.engineerPcb = engineerPcb
        self.year        = year
        self.revision    = revision


    def __repr__(self):
        return '<Assembly: %s, rev %s>' % (self.name, self.revision)


class AssemblyParts(db.Model):
    __tablename__          = 'assembly_part_association'
    part_id                = db.Column(db.Integer, db.ForeignKey('part.id'),     primary_key=True)
    assembly_id            = db.Column(db.Integer, db.ForeignKey('assembly.id'), primary_key=True)
    quantity               = db.Column(db.Integer)

    parts                  = db.relationship(Part, backref="assembly_part_association")
    assembly               = db.relationship(Assembly, backref="assembly_part_association")


    def __init__(self, part, assembly, quantity):
        self.part_id       = part
        self.assembly_id   = assembly
        self.quantity      = quantity

    def __repr__(self):
        return '<Assembly %s Part %s>' % (self.assembly_id, self.part_id)



# class AssemblyParts(db.Model):
#     id               = db.Column(db.Integer, primary_key=True)
#     part_id          = db.Column(db.Integer, db.ForeignKey('part.id'))
#     assembly_id      = db.Column(db.Integer, db.ForeignKey('assembly.id'))
#     count            = db.Column(db.Integer)

#     def __init__(self, part_id, assembly_id, count):
#         self.part_id        = part_id
#         self.description    = description
#         self.count          = count

#     def __repr__(self):
#         return '<Assembly Parts: %s in %s>' % (part_id, assembly_id)