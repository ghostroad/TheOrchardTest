import pytest
from app.models import Establishment, Rating
from sqlalchemy import exc, or_, orm, text
from datetime import date

def test_creation(test_db):
    test_db.add(Establishment(camis=1234, dba="Brasserie Beaubien", ratings = [Rating(grade="A", date="01/02/19")]))
    test_db.commit()
    
    ratings = Rating.query.all()
    assert(len(ratings) == 1)
    rating = ratings[0]
    assert(rating.date == date(2019, 1, 2))
    assert(rating.grade == "A")
            
    
def test_latest_rating(test_db):        
    unrated = Establishment(camis=3456, dba="Pho Lien")
    rated = Establishment(camis=1234, dba="Brasserie Beaubien", ratings=[
        Rating(grade="A", date="01/02/19"), 
        Rating(grade="B", date="03/02/19"), 
        Rating(grade="C", date="02/02/19")
    ])
    test_db.add_all([unrated, rated])
    test_db.commit()

    assert(Establishment.query.get(1234).latest_rating.grade=="B")
    assert(Establishment.query.get(3456).latest_rating is None)
    
def test_filtering_by_latest_rating(test_db):
    poor = Establishment(camis=3456, dba="Pho Lien", ratings=[
        Rating(grade="B", date="01/15/18"),
        Rating(grade="C", date="06/15/18"),
    ])

    okay = Establishment(camis=1234, dba="Brasserie Beaubien", cuisine="French", ratings=[
        Rating(grade="A", date="01/02/19"),
        Rating(grade="B", date="03/02/19"),
        Rating(grade="C", date="02/02/19")
    ])
    
    excellent = Establishment(camis=7654, dba="Trou de Beigne", cuisine="French", ratings=[
        Rating(grade="A", date="04/02/19"),
        Rating(grade="C", date="02/02/19")
    ])

    test_db.add_all([poor, okay, excellent])
    test_db.commit()

    okay_establishments = Establishment.query.options(orm.joinedload(Establishment.latest_rating, innerjoin=True)).filter(
        or_(text("grade='B'"),  text("grade='A'"), Establishment.cuisine == "French")
    ).all()

    assert(set(okay_establishments) == {okay, excellent})
    assert(set(establishment.latest_rating.grade for establishment in okay_establishments) == {"A", "B"})
