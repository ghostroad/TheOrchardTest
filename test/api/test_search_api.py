import pytest
from sietsema.models import Establishment, Rating, LatestRating
from sqlalchemy import or_

def test_searching_by_cuisine_and_minimum_grade(test_client, repo):
    repo.save(
        Establishment(camis=3456, dba="Pho Lien", cuisine="Vietnamese", ratings=[
                Rating(grade="C", date="01/15/18"),
                Rating(grade="B", date="06/15/18"),
            ]),      
        Establishment(camis=1234, dba="Brasserie Beaubien", cuisine="French", ratings=[
                Rating(grade="A", date="01/02/19"),
                Rating(grade="C", date="02/02/19"),
                Rating(grade="B", date="03/02/19"),
            ]),
        Establishment(camis=2345, dba="Gus", cuisine="French", ratings=[
                Rating(grade="C", date="02/02/19"),
                Rating(grade="A", date="04/02/19")
            ]),
        Establishment(camis=7654, dba="Trou de Beigne", cuisine="French", ratings=[
                Rating(grade="A", date="02/02/19"),
                Rating(grade="C", date="04/02/19")
            ]),            
        Establishment(camis=8956, dba="Au Pied de Cochon", cuisine="French", ratings=[
                Rating(grade="C", date="02/02/19"),
                Rating(grade="B", date="04/02/19")
            ]),
        Establishment(camis=9876, dba="Un Chien Fumant", cuisine="French", ratings=[
                Rating(grade="B", date="02/02/19"),
                Rating(grade="A", date="04/02/19")
            ])           
    )
    
    response1 = test_client.get('/search?min_grade=B&after=1234&limit=2&cuisine=French')
    assert response1.status_code == 200    
    assert [elem['dba'] for elem in response1.get_json()] == ["Gus", "Au Pied de Cochon"]
    
    
    response2 = test_client.get('/search?min_grade=B&after=2345&limit=3&cuisine=French')
    assert [elem['dba'] for elem in response2.get_json()] == ["Au Pied de Cochon", "Un Chien Fumant"]
    