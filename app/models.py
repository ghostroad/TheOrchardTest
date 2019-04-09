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
    ratings = db.relationship('Rating', lazy='dynamic')
    
    def __repr__(self):
        return '<Establishment - camis: {}, name: {}>'.format(self.camis, self.dba)
        
class Rating(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(ENUM("A", "B", "C", name="grade", create_type=False), nullable=False)
    date = db.Column(db.Date, nullable=False)
    camis = db.Column(db.Integer, db.ForeignKey('establishment.camis'), nullable=False)
    __table_args__ = (db.UniqueConstraint('camis', 'date'),)
    
    def __repr__(self):
        return '<Rating - camis: {}, date: {}, grade: {}>'.format(self.camis, self.date, self.grade)

ratings_partition = db.select([Rating, db.func.row_number().over(order_by=Rating.date.desc(), partition_by=Rating.camis).label('index')]).alias()

LatestRating = db.aliased(Rating, ratings_partition)

Establishment.latest_rating = db.relationship(
    LatestRating, 
    primaryjoin=db.and_(LatestRating.camis == Establishment.camis, ratings_partition.c.index == 1),
    uselist=False
)