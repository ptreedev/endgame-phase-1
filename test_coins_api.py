def test_GET_all_coins(client):
    response = client.get('/coins')
    assert response.status_code == 200
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
    dupe_coin = {
        'name': 'automate',
        'description': 'automation'
    }
    response = client.post('/coins', json = dupe_coin)
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_DELETE_coin_by_id(client):
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.delete(f'/coin/{coin_id}')
    assert response.status_code == 204
    # try to delete by id again to test error
    response_2 = client.delete(f'/coin/{coin_id}')
    assert response_2.status_code == 404

def test_PATCH_coin_name_by_id(client):
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
    patch_body = { }    
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json = patch_body)
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_PATCH_coin_invalid_field(client):
    patch_body = {
        'invalid_field': 'some_value'
    }    
    coins = client.get('/coins')
    coin_id = coins.get_json()[0]['id']
    response = client.patch(f'/coin/{coin_id}', json = patch_body)
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_PATCH_coin_invalid_id(client):
    patch_body = {
        'name': 'autoauto'
    }    
    invalid_id = 9999
    response = client.patch(f'/coin/{invalid_id}', json = patch_body)
    assert response.status_code == 404