from sietsema import db
from sqlalchemy.dialects.postgresql import ENUM


class Establishment(db.Model):
    camis = db.Column(db.Integer, primary_key=True)
    dba = db.Column(db.String(), nullable=False)
    boro = db.Column(db.String())
    building = db.Column(db.String())
    street = db.Column(db.String())
    zipcode = db.Column(db.String())
    phone = db.Column(db.String())
    inspection_date = db.Column(db.Date)
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


latest_ratings_view = db.select([Rating]).distinct(Rating.camis).order_by(Rating.camis, Rating.date.desc()).alias()

LatestRating = db.aliased(Rating, latest_ratings_view)

Establishment.latest_rating = db.relationship(
    LatestRating, 
    primaryjoin=db.and_(LatestRating.camis == Establishment.camis),
    uselist=False
)
