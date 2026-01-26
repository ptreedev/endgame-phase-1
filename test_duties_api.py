    # test 1 coin and 1 duty relationship
    # if calling a coin it should bring back assciated duties
    # duties: [{
    #     id: uuid
    #     name: string
    #     description: string
    # }, ...]
    # if calling a duty it should bring back associated coins

def test_get_all_duties(client):
    response = client.get('/duties')
    assert response.status_code == 200
    assert 'D1' in response.text
    assert 'duty 1' in response.text

def test_get_duty_by_id(client):
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

def test_get_duty_by_invalid_id(client):
    invalid_id = 9999
    response = client.get(f'/duty/{invalid_id}')
    assert response.status_code == 404
    assert 'Resource not found' in response.text

def test_create_duty(client):
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
        