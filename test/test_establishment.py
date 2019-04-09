import pytest
from app.models import Establishment, Rating
from sqlalchemy import exc

def test_creation(repo):
    repo.save(Establishment(camis = 1234, dba = "Brasserie Beaubien"))
    
    assert(len(Establishment.query.all()) == 1)
    
def test_uniqueness_of_camis_is_enforced(repo):
    with pytest.raises(exc.IntegrityError):
        repo.save(
            Establishment(camis = 1234, dba = "Brasserie Beaubien"), 
            Establishment(camis = 1234, dba = "Next Door")
        )
        
def test_latest_rating(repo):        
    repo.save(Establishment(camis=3456, dba="Pho Lien"))
    repo.save(Establishment(camis=1234, dba="Brasserie Beaubien", ratings=[
        Rating(grade="A", date="01/02/19"), 
        Rating(grade="B", date="03/02/19"), 
        Rating(grade="C", date="02/02/19")
    ]))

    assert(Establishment.query.get(1234).latest_rating.grade=="B")
    assert(Establishment.query.get(3456).latest_rating is None)