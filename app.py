from flask import Flask
from db import connect_to_db, postgres_db

app = Flask(__name__)

@app.before_request
def _db_connect():
    connect_to_db(app)

@app.teardown_request
def _db_close(exc):
    if not postgres_db.is_closed():
        postgres_db.close()

@app.get('/coins')
def get_all_coins():
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)


