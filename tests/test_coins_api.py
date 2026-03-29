
from tests.utils.auth import login, login_admin, register


def test_GET_all_coins(client):
    response = client.get('/coins')
    assert response.status_code == 200
    assert 'automate' in response.text
    assert 'automation' in response.text
    assert 'false' in response.text

def test_GET_all_coins_gets_associated_duties(client):
    login_admin(client)
    new_duty = {
        'name': 'D3',
        'description': 'duty 3'
    }
    duty_response = client.post('/duties', json=new_duty)
    duty_id = duty_response.get_json()['id']

    new_coin = {
        'name': 'houston',
        'description': 'houstonary'
    }
    coin_response = client.post('/coins', json=new_coin)
    coin_id = coin_response.get_json()['id']

    client.patch(f'/coin/{coin_id}/duties', json={'duty_id': duty_id})

    response = client.get('/coins')
    assert response.status_code == 200

    coin_data = response.get_json()
    coin = next((c for c in coin_data if c['id'] == coin_id), None)

    assert coin is not None
    assert coin['name'] == 'houston'
    assert coin['description'] == 'houstonary'
    assert 'duties' in coin
    assert any(duty['id'] == duty_id for duty in coin['duties'])

    assert 'automate' in response.text
    assert 'automation' in response.text

def test_GET_coin_by_id(client):
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.get(f'/coin/{coin_id}')
    expected_id = f'{coin_id}'
    expected_name = 'automate'
    expected_desc = 'automation'
    assert response.status_code == 200
    assert expected_id in response.text
    assert expected_name in response.text
    assert expected_desc in response.text

def test_GET_coin_by_invalid_id(client):
    invalid_id = 9999
    response = client.get(f'/coin/{invalid_id}')
    assert response.status_code == 404

def test_POST_coin(client):
    login_admin(client)
    new_coin = {
        'name': 'houston',
        'description': 'houstonation'
    }
    response = client.post('/coins', json = new_coin)
    created_coin = response.data.decode()
    assert response.status_code == 201
    for column, row in new_coin.items():
        assert column in created_coin
        assert row in created_coin

def test_POST_coin_no_duplication(client):
    login_admin(client)
    dupe_coin = {
        'name': 'automate',
        'description': 'automation'
    }
    response = client.post('/coins', json = dupe_coin)
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_POST_coin_missing_field(client):
    login_admin(client)
    incomplete_coin = {
        'name': 'banana'
    }
    response = client.post('/coins', json = incomplete_coin)
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_DELETE_coin_by_id(client):
    login_admin(client)
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.delete(f'/coin/{coin_id}')
    assert response.status_code == 204
    # try to delete by id again to test error
    response_2 = client.delete(f'/coin/{coin_id}')
    assert response_2.status_code == 404

def test_PATCH_coin_name_by_id(client):
    login_admin(client)
    patch_body = {
        'name': 'autoauto'
    }
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json = patch_body)
    assert response.status_code == 200
    assert 'autoauto' in response.text
    assert 'automation' in response.text

def test_PATCH_coin_desc_by_id(client):
    login_admin(client)
    patch_body = {
        'description': 'bananation'
    }
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json = patch_body)
    updated_coin = response.data.decode()
    assert response.status_code == 200
    assert 'automate' in updated_coin
    assert 'bananation' in updated_coin

def test_PATCH_coin_2_fields(client):
    login_admin(client)
    patch_body = {
        'name': 'autoauto',
        'description': 'bananation'
    }    
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json = patch_body)
    assert response.status_code == 200
    assert 'autoauto' in response.text
    assert 'bananation' in response.text

def test_PATCH_coin_no_fields(client):
    login_admin(client)
    patch_body = { }    
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json = patch_body)
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_PATCH_coin_invalid_field(client):
    login_admin(client)
    patch_body = {
        'invalid_field': 'some_value'
    }    
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json = patch_body)
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_PATCH_coin_invalid_id(client):
    login_admin(client)
    patch_body = {
        'name': 'autoauto'
    }    
    invalid_id = 9999
    response = client.patch(f'/coin/{invalid_id}', json = patch_body)
    assert response.status_code == 404

def test_PATCH_coin_update_complete(client):
    login_admin(client)
    patch_body = {
        'complete': 'true'
    }    
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json = patch_body)
    assert response.status_code == 200
    assert 'true' in response.text
    assert 'automate' in response.text
    assert 'automation' in response.text

def test_PATCH_coin_non_admin_user_can_update_complete_field(client):
    register(client)
    patch_body = {
        'complete': 'true'
    }    
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json = patch_body)
    assert response.status_code == 200
    assert 'true' in response.text
    assert 'automate' in response.text
    assert 'automation' in response.text


def test_PATCH_coin_non_admin_user_returns_403_when_patching_other_fields(client):
    register(client)
    patch_body = {
        'name': 'autoauto',
        'description': 'bananation'
    }    
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json = patch_body)
    assert response.status_code == 403
    assert 'forbidden' in response.text

def test_POST_coin_unknown_field_returns_400(client):
    login_admin(client)
    response = client.post('/coins', json={
        'name': 'houston',
        'description': 'houstonation',
        'malicious': 'value'
    })
    assert response.status_code == 400
    assert 'bad request' in response.text
 
def test_PATCH_coin_unknown_field_returns_400(client):
    login_admin(client)
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json={'unknown_field': 'value'})
    assert response.status_code == 400
    assert 'bad request' in response.text
 
# Validation — XSS attempt in coin fields returns 400
def test_POST_coin_xss_in_name_returns_400(client):
    login_admin(client)
    response = client.post('/coins', json={
        'name': '<script>alert(1)</script>',
        'description': 'valid description'
    })
    assert response.status_code == 400
    assert 'bad request' in response.text
 
def test_POST_coin_xss_in_description_returns_400(client):
    login_admin(client)
    response = client.post('/coins', json={
        'name': 'validname',
        'description': '<img src=x onerror=alert(1)>'
    })
    assert response.status_code == 400
    assert 'bad request' in response.text
 
def test_PATCH_coin_xss_in_name_returns_400(client):
    login_admin(client)
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json={
        'name': '<script>alert(1)</script>'
    })
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_POST_coin_empty_name_returns_400(client):
    login_admin(client)
    response = client.post('/coins', json={
        'name': '',
        'description': 'valid description'
    })
    assert response.status_code == 400
    assert 'bad request' in response.text
 
def test_POST_coin_empty_description_returns_400(client):
    login_admin(client)
    response = client.post('/coins', json={
        'name': 'validname',
        'description': ''
    })
    assert response.status_code == 400
    assert 'bad request' in response.text
 
def test_POST_coin_no_body_returns_400(client):
    login_admin(client)
    response = client.post('/coins', json={})
    assert response.status_code == 400
    assert 'bad request' in response.text
 
def test_POST_coin_whitespace_stripped_from_name(client):
    login_admin(client)
    response = client.post('/coins', json={
        'name': '  houston  ',
        'description': 'houstonation'
    })
    assert response.status_code == 201
    assert response.get_json()['name'] == 'houston'
 
def test_POST_coin_whitespace_stripped_from_description(client):
    login_admin(client)
    response = client.post('/coins', json={
        'name': 'houston',
        'description': '  houstonation  '
    })
    assert response.status_code == 201
    assert response.get_json()['description'] == 'houstonation'
 