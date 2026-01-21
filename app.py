from flask import Flask, jsonify
from db import Coin, connect_to_db, PG_DB, database
from playhouse.shortcuts import model_to_dict

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
    formatted_query = [coin for coin in Coin.select().dicts()]
    return jsonify(formatted_query)


if __name__ == '__main__':
    app.run(debug=True)


