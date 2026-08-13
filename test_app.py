import pytest
from app import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_get_empty_todos(client):
    """Test getting todos when list is empty"""
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.json['todos'] == []

def test_create_todo(client):
    """Test creating a todo"""
    response = client.post('/todos', 
                          json={'title': 'Learn CI/CD'})
    assert response.status_code == 201
    assert response.json['title'] == 'Learn CI/CD'
    assert response.json['completed'] == False

def test_create_todo_missing_title(client):
    """Test creating todo without title"""
    response = client.post('/todos', json={})
    assert response.status_code == 400

def test_get_todo(client):
    """Test getting specific todo"""
    # Create a todo first
    client.post('/todos', json={'title': 'Test Todo'})
    
    # Get it
    response = client.get('/todos/1')
    assert response.status_code == 200
    assert response.json['title'] == 'Test Todo'

def test_update_todo(client):
    """Test updating a todo"""
    # Create a todo
    client.post('/todos', json={'title': 'Original'})
    
    # Update it
    response = client.put('/todos/1', 
                         json={'title': 'Updated', 'completed': True})
    assert response.status_code == 200
    assert response.json['title'] == 'Updated'
    assert response.json['completed'] == True

def test_delete_todo(client):
    """Test deleting a todo"""
    # Create a todo
    client.post('/todos', json={'title': 'To Delete'})
    
    # Delete it
    response = client.delete('/todos/1')
    assert response.status_code == 200
    
    # Verify it's gone
    response = client.get('/todos/1')
    assert response.status_code == 404