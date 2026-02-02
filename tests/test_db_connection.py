from app.db import connect_to_db, database
from app.app import app

def test_real_db_connection():
    connect_to_db(app)
    cursor = database.execute_sql("SELECT 1;")
    result = cursor.fetchone()
    assert result[0] == 1
