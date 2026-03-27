from tests.utils.auth import login_admin

# Figure out a way to use fixtures for login_admin even though. I'm already using them in conftest

def test_GET_requests_returns_200(client):
    login_admin(client)
    response = client.get('/requests')
    assert response.status_code == 200

def test_GET_requests_returns_correct_fields(client):
    login_admin(client)
    client.get('/coins')
    response = client.get('/requests')
    data = response.get_json()
    entry = data[0]
    assert 'method' in entry
    assert 'path' in entry
    assert 'timestamp' in entry
    assert 'status_code' in entry

def test_GET_requests_logs_correct_method_code_path(client):
    login_admin(client)
    client.get('/coins')
    response = client.get('/requests')
    data = response.get_json()
    entry = data[0]
    assert entry['method'] == 'GET'
    assert entry['path'] == '/coins'
    assert entry['status_code'] == 200

def test_GET_requests_logs_different_request(client):
    login_admin(client)
    client.get('/duties')
    response = client.get('/requests')
    data = response.get_json()
    entry = data[0]
    assert entry['method'] == 'GET'
    assert entry['path'] == '/duties'
    assert entry['status_code'] == 200

def test_GET_requests_does_not_log_requests_endpoint(client):
    login_admin(client)
    client.get('/requests')
    response = client.get('/requests')
    data = response.get_json()
    # len is now 1 as register endpoint is called
    assert len(data) == 1

def test_GET_requests_logs_only_last_100_requests(client):
    login_admin(client)
    for i in range(150):
        client.get('/coins')
    response = client.get('/requests')
    data = response.get_json()
    assert len(data) == 100

def test_GET_requests_returns_latest_request_first(client):
    login_admin(client)
    client.get('/coins')
    client.get('/duties')
    response = client.get('/requests')
    data = response.get_json()
    entry = data[0]
    assert entry['path'] == '/duties'
