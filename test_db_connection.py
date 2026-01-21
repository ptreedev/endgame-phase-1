from db import connect_to_db, database, PG_DB
from app import app

def test_real_db_connection():
    connect_to_db(app, PG_DB)
    cursor = database.execute_sql("SELECT 1;")
    result = cursor.fetchone()
    assert result[0] == 1
