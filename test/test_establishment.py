import pytest
from app.models import Establishment
from sqlalchemy import exc

def test_creation(test_db):
    test_db.add(Establishment(camis = 1234, dba = "Brasserie Beaubien"))
    test_db.commit()
    
    assert(len(Establishment.query.all()) == 1)
    
def test_uniqueness_of_camis_is_enforced(test_db):
    test_db.add(Establishment(camis = 1234, dba = "Brasserie Beaubien"))
    test_db.add(Establishment(camis = 1234, dba = "Next Door"))
    
    with pytest.raises(exc.IntegrityError):
        test_db.commit()
    
    
    
