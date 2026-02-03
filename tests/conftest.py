import pytest
from app.db import *
from app.app import app


@pytest.fixture(autouse=True)
def setup_test_db():
    connect_to_db(app)
    database.create_tables([Coin, Duty, CoinDuty])
    Coin.create(name='automate', description='automation')
    Duty.create(name='D1', description='duty 1')
    
    yield

    database.drop_tables([Coin, Duty, CoinDuty])
    database.close()

@pytest.fixture(scope='function')
def client(setup_test_db):
    app.testing = True
    with app.test_client() as client:
        yield client