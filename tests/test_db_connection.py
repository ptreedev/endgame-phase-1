from app.db import PG_DB, connect_to_db, database
from app.app import app

def test_real_db_connection():
    # Override the database proxy to use the real Postgres DB
    database.initialize(PG_DB)
    connect_to_db(app)
    cursor = database.execute_sql("SELECT 1;")
    result = cursor.fetchone()
    assert result[0] == 1
    database.close()