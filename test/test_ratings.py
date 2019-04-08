import pytest
from app.models import Establishment, Rating
from sqlalchemy import exc

def test_creation(test_db):
    establishment = Establishment(camis=1234, dba="Brasserie Beaubien")
    establishment.ratings.append(Rating(grade="A", date="01/02/19"))
    test_db.add(establishment)
    test_db.commit()
    
    ratings = Rating.query.all()
    assert(len(ratings) == 1)
    
    rating = ratings[0]
    assert(rating.establishment == establishment)
    assert(rating.grade == "A")
            
    
    
