from tests.utils.auth import register

# Figure out a way to use fixtures for register even though. I'm already using them in conftest

def test_GET_requests_returns_200(client):
    register(client, role='admin')
    response = client.get('/requests')
    assert response.status_code == 200

def test_GET_requests_returns_correct_fields(client):
    register(client, role='admin')
    client.get('/coins')
    response = client.get('/requests')
    data = response.get_json()
    entry = data[0]
    assert 'method' in entry
    assert 'path' in entry
    assert 'timestamp' in entry
    assert 'status_code' in entry

def test_GET_requests_logs_correct_method_code_path(client):
    register(client, role='admin')
    client.get('/coins')
    response = client.get('/requests')
    data = response.get_json()
    entry = data[0]
    assert entry['method'] == 'GET'
    assert entry['path'] == '/coins'
    assert entry['status_code'] == 200

def test_GET_requests_logs_different_request(client):
    register(client, role='admin')
    client.get('/duties')
    response = client.get('/requests')
    data = response.get_json()
    entry = data[0]
    assert entry['method'] == 'GET'
    assert entry['path'] == '/duties'
    assert entry['status_code'] == 200

def test_GET_requests_does_not_log_requests_endpoint(client):
    register(client, role='admin')
    client.get('/requests')
    response = client.get('/requests')
    data = response.get_json()
    # len is now 1 as register endpoint is called
    assert len(data) == 1

def test_GET_requests_logs_only_last_100_requests(client):
    register(client, role='admin')
    for i in range(150):
        client.get('/coins')
    response = client.get('/requests')
    data = response.get_json()
    assert len(data) == 100

def test_GET_requests_returns_latest_request_first(client):
    register(client, role='admin')
    client.get('/coins')
    client.get('/duties')
    response = client.get('/requests')
    data = response.get_json()
    entry = data[0]
    assert entry['path'] == '/duties'
