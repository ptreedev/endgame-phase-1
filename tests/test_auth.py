from tests.utils.auth import login_admin, register, login


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
    user_body = {
        'username': 'superadmin',
        'password': 'password',
        'role': 'superadmin'
    }
    response = client.post('/auth/register', json=user_body)
    assert response.status_code == 400

def test_POST_register_sets_session(client):
    register(client)
    response = client.get('/auth/me')
    data = response.get_json()
    assert response.status_code == 200
    assert data['username'] == 'testuser'
    assert data['role'] == 'user'

# admin_role should not be set from calling the endpoint
def test_POST_register_admin_role_unavailable(client):
    user_body = {
        'username': 'admin',
        'password': 'password',
        'role': 'admin'
    }
    response = client.post('/auth/register', json=user_body)
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'bad request'
    



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

def test_DECORATOR_login_required(client):
    # make request to protected endpoint, 
    # should return 401 if unauth and 200 if auth
    unauth_response = client.get('/auth/me')
    assert unauth_response.status_code == 401
    register(client)
    response = client.get('/auth/me')
    assert response.status_code == 200

def test_DECORATOR_admin_required(client):
    # protect logs endpoint with admin decorator
    register(client)
    unauth_response = client.get('/requests')
    assert unauth_response.status_code == 403
    login_admin(client)
    response = client.get('/requests')
    assert response.status_code == 200

def test_USER_account_locks_after_5_failed_attempts(client):
    register(client)
    for _ in range(5):
        login(client, password="wrongpassword")
    response = login(client, password="wrongpassword")
    assert response.status_code == 423
    assert "account locked" in response.get_json()["message"]

def test_USER_locked_account_rejects_correct_password(client):
    register(client)
    for _ in range(5):
        login(client, password="wrongpassword")
    response = login(client, password="secret123")
    assert response.status_code == 423

def test_USER_failed_attempts_reset_on_successful_login(client):
    register(client)
    for _ in range(3):
        login(client, password="wrongpassword")
    login(client, password="secret123")
    from app.db import User
    user = User.get(User.username == "testuser")
    assert user.failed_attempts == 0
    assert user.locked_until is None

def test_USER_account_not_locked_before_threshold(client):
    register(client)
    for _ in range(4):
        login(client, password="wrongpassword")
    response = login(client, password="secret123")
    assert response.status_code == 200

def test_POST_register_unknown_field_returns_400(client):
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'secret123',
        'extra': 'field'
    })
    assert response.status_code == 400
 
def test_POST_register_short_password_returns_400(client):
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'short'
    })
    assert response.status_code == 400
    assert 'bad request' in response.get_json()['message']
 
def test_POST_register_invalid_username_characters_returns_400(client):
    response = client.post('/auth/register', json={
        'username': 'test user!',
        'password': 'secret123'
    })
    assert response.status_code == 400
    assert 'bad request' in response.get_json()['message']
 
def test_POST_register_xss_username_returns_400(client):
    response = client.post('/auth/register', json={
        'username': '<script>alert(1)</script>',
        'password': 'secret123'
    })
    assert response.status_code == 400
 
def test_POST_register_whitespace_stripped_from_username(client):
    response = client.post('/auth/register', json={
        'username': '  testuser  ',
        'password': 'secret123'
    })
    assert response.status_code == 201
    assert response.get_json()['username'] == 'testuser'
 