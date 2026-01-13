import pytest
from db import *
from app import app

app.testing = True
testApp = app.test_client()

@pytest.fixture(autouse=True)
def setup_table():
    postgres_db.bind([Coin], bind_refs=False, bind_backrefs=False)
    connect_to_db(app)
    postgres_db.create_tables([Coin])
    yield
    postgres_db.drop_tables([Coin])
    postgres_db.close()

def test_get_all_coins():
    response = testApp.get('/coins')
    assert response.status_code is 200