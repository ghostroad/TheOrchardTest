import pytest
from app.models import Establishment, Rating
from sqlalchemy import exc
from datetime import date

def test_creation(test_db):
    establishment = Establishment(camis=1234, dba="Brasserie Beaubien")
    establishment.ratings.append(Rating(grade="A", date="01/02/19"))
    test_db.add(establishment)
    test_db.commit()
    
    ratings = Rating.query.all()
    assert(len(ratings) == 1)
    rating = ratings[0]
    assert(rating.date == date(2019, 1, 2))
    assert(rating.grade == "A")
            
    
def test_latest_rating(test_db):        
    unrated = Establishment(camis=3456, dba="Pho Lien")
    rated = Establishment(camis=1234, dba="Brasserie Beaubien")
    rated.ratings.extend([
        Rating(grade="A", date="01/02/19"), 
        Rating(grade="B", date="03/02/19"), 
        Rating(grade="C", date="02/02/19")
    ])
    test_db.add(unrated)
    test_db.add(rated)
    test_db.commit()

    assert(Establishment.query.get(1234).latest_rating.grade=="B")
    assert(Establishment.query.get(3456).latest_rating is None)