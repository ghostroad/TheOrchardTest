import pytest
from app.models import Establishment
from sqlalchemy import exc

def test_creation(test_db):
    e = Establishment(camis = 1234, dba = "Brasserie Beaubien")
    test_db.add(e)
    test_db.commit()
    
    assert(len(Establishment.query.all()) == 1)
    
def test_uniqueness_of_camis_is_enforced(test_db):
    assert len(Establishment.query.all()) == 0
    e1 = Establishment(camis = 1234, dba = "Brasserie Beaubien")
    e2 = Establishment(camis = 1234, dba = "Next Door")
    
    test_db.add(e1)
    test_db.add(e2)
    with pytest.raises(exc.IntegrityError):
        test_db.commit()
    
    
    
