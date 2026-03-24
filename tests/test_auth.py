def register(client, username="testuser", password="secret123", role="user"):
    return client.post("/auth/register", json={
        "username": username,
        "password": password,
        "role": role
    })

def test_POST_register_user(client):
    response = register(client)
    data = response.data.decode()
    assert response.status_code == 201
    assert 'id' in data
    assert 'testuser' in data
    assert 'user' in data
    assert 'password123' not in data
    assert 'password_hash' not in data

def test_POST_register_no_duplicate_username(client):
    register(client)
    response = register(client)
    assert response.status_code == 400
    assert "bad request" in response.get_json()["message"]

def test_POST_register_missing_username(client):
    response = client.post("/auth/register", json={"password": "secret123"})
    assert response.status_code == 400

def test_POST_register_missing_password(client):
    response = client.post("/auth/register", json={"username": "testuser"})
    assert response.status_code == 400
 
def test_POST_register_invalid_role(client):
    response = register(client, role="superuser")
    assert response.status_code == 400