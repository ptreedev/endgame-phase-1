import pytest
from db import *
from app import app

@pytest.fixture(scope='session')
def setup_test_db():
    connect_to_db(app, TEST_DB)
    TEST_DB.create_tables([Coin])
    Coin.create(name='automate', description='automation')
    
    yield

    TEST_DB.drop_tables([Coin])
    TEST_DB.close()

@pytest.fixture
def client(setup_test_db):
    app.testing = True
    with app.test_client() as client:
        yield client


def test_get_all_coins(client):
    response = client.get("/coins")
    assert response.status_code == 200
    assert 'automate' in response.text
    assert 'automation' in response.text