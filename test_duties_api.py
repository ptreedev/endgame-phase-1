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
