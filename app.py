from flask import Flask, request
from db import Coin, connect_to_db, PG_DB, database
from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError

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

@app.get('/coin/<coin_id>')
def get_coin_by_id(coin_id):
    coin = Coin.get_by_id(coin_id)
    format_coin = model_to_dict(coin)
    return format_coin

@app.post('/coins')
def create_coin():
    try: 
        body = request.get_json()
        created_coin = Coin.create(name = body['name'], description = body['description'])
        return model_to_dict(created_coin), 201
    except IntegrityError:
        error = {'error': 'bad request',
                'message': 'name already exists'}
        return error, 400
    
@app.delete('/coin/<coin_id>')
def delete_coin_by_id(coin_id):
    delete_query = Coin.delete_by_id(coin_id)
    if(delete_query == 0):
        return {'message': 'resource not found'}, 404
    return '', 204

@app.patch('/coin/<coin_id>')
def patch_coin_by_id(coin_id):
    body = request.get_json()

    allowed_fields = {'name', 'description'}
    update_data = {
        getattr(Coin, key): value
        for key, value in body.items()
        if key in allowed_fields
    }

    query = Coin.update(update_data).where(Coin.id == coin_id)
    query.execute()

    updated_coin = model_to_dict(Coin.get_by_id(coin_id))
    return updated_coin, 200


if __name__ == '__main__':
    app.run(debug=True)


