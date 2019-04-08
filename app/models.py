from app import db

class Establishment(db.Model):
    camis = db.Column(db.Integer, primary_key = True)
    dba = db.Column(db.String())
    boro = db.Column(db.String())
    building = db.Column(db.String())
    street = db.Column(db.String())
    zipcode = db.Column(db.String())
    phone = db.Column(db.String())
    cuisine = db.Column(db.String(), index = True)
    
    def __repr__(self):
        return '<Establishment - camis: {}, name: {}>'.format(self.camis, self.dba)