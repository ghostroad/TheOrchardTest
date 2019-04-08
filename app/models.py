from app import db
from sqlalchemy.dialects.postgresql import ENUM

class Establishment(db.Model):
    camis = db.Column(db.Integer, primary_key=True)
    dba = db.Column(db.String())
    boro = db.Column(db.String())
    building = db.Column(db.String())
    street = db.Column(db.String())
    zipcode = db.Column(db.String())
    phone = db.Column(db.String())
    cuisine = db.Column(db.String(), index=True)
    ratings = db.relationship('Rating', backref='establishment', lazy='dynamic')
    
    def __repr__(self):
        return '<Establishment - camis: {}, name: {}>'.format(self.camis, self.dba)
        
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(ENUM("A", "B", "C", name="grade", create_type=False), nullable=False)
    date = db.Column(db.Date, nullable=False)
    camis = db.Column(db.Integer, db.ForeignKey('establishment.camis'), nullable=False)
    
    def __repr__(self):
        return '<Rating - camis: {}, date: {}, grade: {}>'.format(self.camis, self.date, self.grade)
    