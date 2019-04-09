import json
from sietsema.models import Establishment

def test_health(test_client):
    response = test_client.get('/health')
    assert response.status_code == 200
    
def test_creating_an_establishment(test_client, repo):
    data = {'dba': 'La Banquisse', 'phone': '4384056262'}
    response = test_client.put('/establishments/1234', json=data)
    assert response.status_code == 200
    
    assert "Created" in json.loads(response.data)['message']
    
    assert repo.find(1234).dba == 'La Banquisse'

def test_creating_an_establishment_fails_when_given_invalid_key(test_client, repo):
    data = {'dba': 'La Banquisse', 'phone': '4384056262', 'whatever': 'nonsense'}
    response = test_client.put('/establishments/1234', json=data)
    assert response.status_code == 400
    
    assert "invalid key" in json.loads(response.data)['message']
    
    assert repo.find(1234) is None


def test_updating_an_establishment(test_client, repo):
    response = test_client.put('/establishments/1234', json={'dba': 'La Banquisse', 'zipcode': '02093', 'phone': '4384056262'})
    assert response.status_code == 200

    response = test_client.put('/establishments/1234', json={'dba': 'Romado', 'phone': '4384056363'})
    assert response.status_code == 200
    
    assert "Updated" in json.loads(response.data)['message']
    
    romado = repo.find(1234)
    assert romado.dba == 'Romado'
    assert romado.phone == '4384056363'
    assert romado.zipcode == '02093'

def test_establishments_must_have_a_nonempty_dba(test_client, repo):
    response = test_client.put('/establishments/1234', json={'dba': '', 'phone': '4384056262'})
    assert response.status_code == 400

    assert "The 'dba' field cannot be empty." in json.loads(response.data)['message']       
    
def test_creating_a_rating(test_client, repo):
    repo.save(Establishment(camis=1234, dba='Adamo'))
    test_client.put('/establishments/1234/ratings', json={'dba': '', 'phone': '4384056262'}, content_type='application/json')
    
     