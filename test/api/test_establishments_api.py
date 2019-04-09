def test_health(test_client):
    response = test_client.get('/health')
    assert response.status_code == 200
    
def test_creating_an_establishment(test_client, repo):
    response = test_client.put('/establishments/1234', json={'dba': 'La Banquisse', 'phone': '4384056262'})
    assert response.status_code == 200
    
    assert "Created" in response.get_json()['message']
    
    assert repo.find(1234).dba == 'La Banquisse'

def test_creating_an_establishment_fails_when_given_invalid_key(test_client, repo):
    data = {'dba': 'La Banquisse', 'phone': '4384056262', 'whatever': 'nonsense'}
    response = test_client.put('/establishments/1234', json=data)
    assert response.status_code == 400
    
    assert "invalid key" in response.get_json()['message']
    
    assert repo.find(1234) is None
    
def test_updating_an_establishment_does_nothing_with_stale_info(test_client, repo):
    response1 = test_client.put('/establishments/1234', json={'dba': 'La Banquisse', 'zipcode': '02093', 'phone': '4384056262', 'inspection_date': '02/01/19'})
    assert response1.status_code == 200
    
    response2 = test_client.put('/establishments/1234', json={'dba': 'Romado', 'inspection_date': '01/01/19'})
    assert "Must provide an inspection date that is newer" in response2.get_json()['message']
    assert response2.status_code == 403
    
    assert repo.find(1234).dba == 'La Banquisse' 
    
def test_updating_an_establishment(test_client, repo):
    response = test_client.put('/establishments/1234', json={'dba': 'La Banquisse', 'zipcode': '02093', 'phone': '4384056262'})
    assert response.status_code == 200

    response = test_client.put('/establishments/1234', json={'dba': 'Romado', 'phone': '4384056363', 'inspection_date': '01/01/19'})
    assert response.status_code == 200
    assert "Updated" in response.get_json()['message']
    
    romado = repo.find(1234)
    assert romado.dba == 'Romado'
    assert romado.phone == '4384056363'
    assert romado.zipcode == '02093'

def test_establishments_must_have_a_nonempty_dba(test_client, repo):
    response = test_client.put('/establishments/1234', json={'dba': '', 'phone': '4384056262'})
    assert response.status_code == 400

    assert "The 'dba' field cannot be empty." in response.get_json()['message']       
    
