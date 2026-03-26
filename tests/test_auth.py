def register(client, username='testuser', password='secret123', role='user'):
    return client.post('/auth/register', json={
        'username': username,
        'password': password,
        'role': role
    })

def login(client, username='testuser', password='secret123', role='user'):
    return client.post('/auth/login', json={
        'username': username,
        'password': password,
        'role': role
    })

def test_POST_register_user(client):
    response = register(client)
    data = response.data.decode()
    assert response.status_code == 201
    assert 'id' in data
    assert 'testuser' in data
    assert 'user' in data
    assert 'secret123' not in data
    assert 'password_hash' not in data

def test_POST_register_no_duplicate_username(client):
    register(client)
    response = register(client)
    assert response.status_code == 400
    assert 'bad request' in response.get_json()['message']

def test_POST_register_missing_username(client):
    response = client.post('/auth/register', json={'password': 'secret123'})
    assert response.status_code == 400

def test_POST_register_missing_password(client):
    response = client.post('/auth/register', json={'username': 'testuser'})
    assert response.status_code == 400
 
def test_POST_register_invalid_role(client):
    response = register(client, role='superuser')
    assert response.status_code == 400

def test_POST_register_sets_session(client):
    register(client)
    response = client.get('/auth/me')
    data = response.get_json()
    assert response.status_code == 200
    assert data['username'] == 'testuser'
    assert data['role'] == 'user'


def test_POST_login(client):
    register(client)
    response = login(client)
    data = response.data.decode()
    assert response.status_code == 200
    assert 'id' in data
    assert 'testuser' in data
    assert 'user' in data
    assert 'secret123' not in data
    assert 'password_hash' not in data

def test_POST_login_wrong_password(client):
    register(client)
    response = login(client, password='wrongpassword')
    assert response.status_code == 401
    assert 'invalid credentials' in response.get_json()['message']

def test_POST_login_unknown_user(client):
    response = login(client, username='nobody')
    assert response.status_code == 401
    assert 'invalid credentials' in response.get_json()['message']

def test_GET_me_returns_user(client):
    register(client)
    login(client)
    response = client.get('/auth/me')
    data = response.get_json()
    assert response.status_code == 200
    assert data['username'] == 'testuser'
    assert data['role'] == 'user'

def test_POST_login_missing_fields(client):
    response = client.post('/auth/login', json={'username': 'testuser'})
    assert response.status_code == 400

def test_POST_logout_returns_200_and_clears_session(client):
    register(client)
    response = client.post('/auth/logout')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'logged out'