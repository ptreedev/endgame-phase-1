from tests.consts import USERNAME, PASSWORD

def register(client, username='testuser', password='secret123'):
    return client.post('/auth/register', json={
        'username': username,
        'password': password,
    })

def login(client, username='testuser', password='secret123'):
    return client.post('/auth/login', json={
        'username': username,
        'password': password,
    })

def login_admin(client, username=USERNAME, password=PASSWORD):
        return client.post('/auth/login', json={
        'username': username,
        'password': password,
    })