    # test 1 coin and 1 duty relationship
    # if calling a coin it should bring back assciated duties
    # duties: [{
    #     id: uuid
    #     name: string
    #     description: string
    # }, ...]
    # if calling a duty it should bring back associated coins

def test_GET_all_duties(client):
    response = client.get('/duties')
    assert response.status_code == 200
    assert 'D1' in response.text
    assert 'duty 1' in response.text

def test_GET_duty_by_id(client):
    duties = client.get('/duties')
    duty_id = duties.get_json()[0]['id']
    response = client.get(f'/duty/{duty_id}')
    expected_id = f'{duty_id}'
    expected_name = 'D1'
    expected_desc = 'duty 1'
    assert response.status_code == 200
    assert expected_id in response.text
    assert expected_name in response.text
    assert expected_desc in response.text

def test_GET_duty_by_invalid_id(client):
    invalid_id = 9999
    response = client.get(f'/duty/{invalid_id}')
    assert response.status_code == 404
    assert 'Resource not found' in response.text

def test_POST_duty(client):
    new_duty = {
        'name': 'D2',
        'description': 'duty 2'
    }
    response = client.post('/duties', json=new_duty)
    created_duty = response.data.decode()
    assert response.status_code == 201
    for column, row in new_duty.items():
        assert column in created_duty
        assert row in created_duty

def test_POST_duty_no_duplication(client):
    dupe_duty = {
        'name': 'D1',
        'description': 'duty 1'
    }
    response = client.post('/duties', json=dupe_duty)
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_POST_duty_missing_field(client):
    incomplete_duty = {
        'name': 'D3'
    }
    response = client.post('/duties', json=incomplete_duty)
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_DELETE_duty_by_id(client):
    duties = client.get('/duties')
    duty_id = duties.get_json()[0]['id']
    response = client.delete(f'/duty/{duty_id}')
    assert response.status_code == 204
    response_2 = client.delete(f'/duty/{duty_id}')
    assert response_2.status_code == 404

def test_PATCH_duty_one_field(client):
    patch_body = {
        'name': 'D1-partial-update'
    }    
    duties = client.get('/duties')
    duty_id = duties.get_json()[0]['id']
    response = client.patch(f'/duty/{duty_id}', json=patch_body)
    updated_duty = response.data.decode()
    assert response.status_code == 200
    assert 'D1-partial-update' in updated_duty
    assert 'duty 1' in updated_duty

def test_PATCH_duty_by_id(client):
    patch_body = {
        'name': 'D1-updated',
        'description': 'duty 1 updated'
    }    
    duties = client.get('/duties')
    duty_id = duties.get_json()[0]['id']
    response = client.patch(f'/duty/{duty_id}', json=patch_body)
    updated_duty = response.data.decode()
    assert response.status_code == 200
    assert 'D1-updated' in updated_duty
    assert 'duty 1 updated' in updated_duty

def test_PATCH_duty_no_fields(client):
    patch_body = { }    
    duties = client.get('/duties')
    duty_id = duties.get_json()[0]['id']
    response = client.patch(f'/duty/{duty_id}', json=patch_body)
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_PATCH_duty_invalid_field(client):
    patch_body = {
        'invalid_field': 'some_value'
    }    
    duties = client.get('/duties')
    duty_id = duties.get_json()[0]['id']
    response = client.patch(f'/duty/{duty_id}', json=patch_body)
    assert response.status_code == 400
    assert 'bad request' in response.text

def test_PATCH_duty_invalid_id(client):
    patch_body = {
        'name': 'D1-updated'
    }    
    invalid_id = 9999
    response = client.patch(f'/duty/{invalid_id}', json=patch_body)
    assert response.status_code == 404
    assert 'Resource not found' in response.text

def test_GET_duty_returns_associated_coins(client):
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

    association_body = {
        'duty_id': duty_id
    }
    client.patch(f'/coin/{coin_id}/duties', json=association_body)
    expected_response = {
        'id': duty_id,
        'name': 'D3',
        'description': 'duty 3',
        'coins': [{
            'id': coin_id,
            'name': 'houston',
            'description': 'houstonary'
        }]
    }
    response = client.get(f'/duty/{duty_id}/coins')
    duty_data = response.get_json()
    assert response.status_code == 200
    for key, value in expected_response.items():
        if key != 'coins':
            assert key in duty_data.keys()
            assert value in duty_data.values()
        elif key == 'coins':
            assert any(coin['id'] == coin_id for coin in duty_data['coins'])