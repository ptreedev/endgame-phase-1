import pytest
from app.db import *
from app.app import app
from tests.consts import USERNAME, PASSWORD


@pytest.fixture()
def setup_test_db():
    connect_to_db(app)
    database.create_tables([Coin, Duty, CoinDuty, RequestLog, User])
    Coin.create(name='automate', description='automation')
    Duty.create(name='D1', description='duty 1')
    admin = User(username=USERNAME, role=User.ROLE_ADMIN)
    admin.set_password(PASSWORD)
    admin.save(force_insert=True)
    
    yield

    database.drop_tables([Coin, Duty, CoinDuty, RequestLog, User])
    database.close()

@pytest.fixture(scope='function')
def client(setup_test_db):
    app.testing = True
    with app.test_client() as client:
        yield client
