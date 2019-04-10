from sietsema.models import Establishment

def test_creating_a_rating(test_client, repo):
    repo.save(Establishment(camis=1234, dba='Adamo'))
    response = test_client.post('/establishments/1234/ratings', json={'grade': 'A', 'date': '02/10/2019'})
    assert response.status_code == 200
    
    assert repo.find(1234).ratings[0].grade == 'A'
    
def test_creating_a_rating_fails_if_no_establishment_found(test_client, repo):
    response = test_client.post('/establishments/1234/ratings', json={'grade': 'A', 'date': '02/10/2019'})
    assert response.status_code == 400
    
    assert "No establishment with that camis exists." in response.get_json()['message']       

def test_creating_a_rating_fails_if_some_field_is_missing(test_client, repo):
    test_client.put('/establishments/1234', json={'dba': 'La Banquisse', 'phone': '4384056262'})
    
    response = test_client.post('/establishments/1234/ratings', json={'date': '02/10/2019'})
    assert response.status_code == 400
    
    assert "The 'grade' field cannot be empty." in response.get_json()['message']       


def test_creating_a_rating_fails_if_some_field_is_invalid(test_client, repo):
    test_client.put('/establishments/1234', json={'dba': 'La Banquisse', 'phone': '4384056262'})
    
    response = test_client.post('/establishments/1234/ratings', json={'grade': 'W', 'date': '02/10/2019'})
    assert response.status_code == 400
    
    assert "The grade must be A, B, or C." in response.get_json()['message']
        
def test_creating_a_rating_fails_if_there_is_one_for_that_date(test_client, repo):
    test_client.put('/establishments/1234', json={'dba': 'La Banquisse', 'phone': '4384056262'})
    test_client.post('/establishments/1234/ratings', json={'grade': 'A', 'date': '02/10/2019'})
    
    response = test_client.post('/establishments/1234/ratings', json={'grade': 'B', 'date': '02/10/2019'})
    assert response.status_code == 403
    
    assert "A rating already exists for that date." in response.get_json()['message']
        
          