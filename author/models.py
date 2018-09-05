from Stock_Manager import db

class Author(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    fullname            = db.Column(db.String(80))
    email               = db.Column(db.String(35), unique=True)
    username            = db.Column(db.String(25), unique=True)
    password            = db.Column(db.String(60))
    authorization_level = db.Column(db.Integer)
    # authorization levels:
    # 0 - passive (restrited access, read only)
    # 1 - member  (restricted access)
    # 2 - mod (extended access)
    # 3 - admin (full access)

    # posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def __init__(self, fullname, email, username, password, authorization_level=1):
        self.fullname               = fullname
        self.email                  = email
        self.username               = username
        self.password               = password
        self.authorization_level    = authorization_level

    def __repr__(self):
        return '<Author %r>' % self.username
