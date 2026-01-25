import pytest
from db import *
from app import app


@pytest.fixture(autouse=True)
def setup_test_db():
    connect_to_db(app, TEST_DB)
    TEST_DB.create_tables([Coin])
    Coin.create(name='automate', description='automation')
    
    yield

    TEST_DB.drop_tables([Coin])
    TEST_DB.close()

@pytest.fixture(scope='function')
def client(setup_test_db):
    app.testing = True
    with app.test_client() as client:
        yield client


def test_get_all_coins(client):
    response = client.get('/coins')
    assert response.status_code == 200
    assert 'automate' in response.text
    assert 'automation' in response.text

def test_get_coin_by_id(client):
    coins = client.get('/coins')
    coins_id = coins.get_json()[0]['id']
    response = client.get(f'/coins/{coins_id}')
    expected_id = f'{coins_id}'
    expected_name = 'automate'
    expected_desc = 'automation'
    assert response.status_code == 200
    assert expected_id in response.text
    assert expected_name in response.text
    assert expected_desc in response.text

def test_create_coin(client):
    new_coin = {
        'name': 'houston',
        'description': 'houstonation'
    }
    response = client.post('/coins', json = new_coin)
    created_coin = response.data.decode()
    assert response.status_code is 201
    for column, row in new_coin.items():
        assert column in created_coin
        assert row in created_coin

def test_create_coin_no_duplication(client):
    dupe_coin = {
        'name': 'automate',
        'description': 'automation'
    }
    response = client.post('/coins', json = dupe_coin)
    assert response.status_code == 400
    assert 'bad request' in response.text
    