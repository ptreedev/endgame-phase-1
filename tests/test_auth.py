def test_POST_register_user(client):
    user = {
        'username': 'testuser',
        'password': 'password123',
        'role': 'user'
    }
    response = client.post("/auth/register", json = user)
    data = response.data.decode()
    assert response.status_code == 201
    assert 'id' in data
    assert 'testuser' in data
    assert 'user' in data
    assert 'password123' not in data
    assert 'password_hash' not in data
