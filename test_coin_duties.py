def test_PATCH_COIN_associate_coin_duty(client):
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

    association_response = client.patch(f'/coin/{coin_id}/duties', json={
        'duty_id': duty_id
    })
    assert association_response.status_code == 200
    assert association_response.get_json() == {
        'message': 'Association created successfully'
    }
