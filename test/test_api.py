
def test_health(test_client):
    response = test_client.get('/health')
    assert response.status_code == 200
    

def test_creating_an_establishment(test_client, repo):
    data = {'dba': 'La Banquisse', 'phone': '4384056262'}
    response = test_client.put('/establishment/1234', json=data, content_type='application/json')
    assert response.status_code == 200
    
    assert(repo.find(1234).dba == 'La Banquisse')
    