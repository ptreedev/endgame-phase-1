import pytest
from db import *
from app import app


@pytest.fixture(autouse=True)
def setup_test_db():
    connect_to_db(app, TEST_DB)
    TEST_DB.create_tables([Coin, Duty])
    Coin.create(name='automate', description='automation')
    Duty.create(name='D1', description='duty 1')
    
    yield

    TEST_DB.drop_tables([Coin, Duty])
    TEST_DB.close()

@pytest.fixture(scope='function')
def client(setup_test_db):
    app.testing = True
    with app.test_client() as client:
        yield client