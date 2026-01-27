def test_POST_associate_coin_duty(client):
    new_duty = {
        'name': 'D2',
        'description': 'duty 2'
    }
    duty_response = client.post('/duties', json=new_duty)
    assert duty_response.status_code == 201
    created_duty = duty_response.get_json()
    duty_id = created_duty['id']

    new_coin = {
        'name': 'secure',
        'description': 'security'
    }
    coin_response = client.post('/coins', json=new_coin)
    created_coin = coin_response.get_json()
    coin_id = created_coin['id']

    association_response = client.post('/coin_duties', json={
        'coin_id': coin_id,
        'duty_id': duty_id
    })
    assert association_response.status_code == 201
    assert association_response.get_json() == {
        'message': 'Association created successfully'
    }

def test_POST_associate_coin_duty_invalid_ids(client):
    association_response = client.post('/coin_duties', json={
        'coin_id': 'non-existent-coin-id',
        'duty_id': 'non-existent-duty-id'
    })
    assert association_response.status_code == 404
    assert association_response.get_json() == {
        'message': 'Resource not found'
    }