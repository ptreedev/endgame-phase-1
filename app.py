from flask import Flask
from db import connect_to_db, PG_DB, database

app = Flask(__name__)

@app.before_request
def _db_connect():
    if not app.testing:
        connect_to_db(app, PG_DB)

@app.teardown_request
def _db_close(exc):
    if not database.is_closed():
        database.close()

@app.get('/coins')
def get_all_coins():
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)


