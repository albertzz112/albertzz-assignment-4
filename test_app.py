import pytest
from app import app

# Test search functionality
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_search(client):
    # Simulate a search request
    response = client.post('/search', data={'query': 'computer'})
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert 'documents' in json_data
    assert 'similarities' in json_data
    assert 'indices' in json_data
    assert len(json_data['documents']) == 5  # Checking that we get 5 results
