from sietsema.models import Establishment, LatestRating
from sqlalchemy import orm


class EstablishmentRepository(object):
    
    def __init__(self, db):
        self.db = db
    
    def latest_ratings_query(self):
        return self.db.query(Establishment).\
            join(Establishment.latest_rating).\
            options(orm.contains_eager(Establishment.latest_rating, alias=LatestRating))
    
    def save(self, *establishments):
        self.db.add_all(establishments)
        self.db.commit()
        
    def find(self, camis):
        return Establishment.query.get(camis)
