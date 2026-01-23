from flask import Flask, request
from db import Coin, connect_to_db, PG_DB, database
from playhouse.shortcuts import model_to_dict

app = Flask(__name__)

@app.before_request
def _db_connect():
    if not app.testing:
        connect_to_db(app, PG_DB)

@app.teardown_request
def _db_close(exc):
    if not app.testing and not database.is_closed():
        database.close()

@app.get('/coins')
def get_all_coins():
    formatted_query = [coin for coin in Coin.select().dicts()]
    return formatted_query

@app.get('/coins/<coin_id>')
def get_coin_by_id(coin_id):
    coin = Coin.get_by_id(coin_id)
    format_coin = model_to_dict(coin)
    return format_coin

@app.post('/coins')
def create_coin():
    body = request.get_json()
    created_coin = Coin.create(name = body['name'], description = body['description'])
    return model_to_dict(created_coin), 201

if __name__ == '__main__':
    app.run(debug=True)


