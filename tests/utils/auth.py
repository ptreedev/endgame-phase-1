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