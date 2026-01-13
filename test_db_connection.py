from db import connect_to_db
from app import app

def test_real_db_connection():
    connect_to_db(app)