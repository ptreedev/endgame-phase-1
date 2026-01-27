from flask import Flask, request
from db import Coin, CoinDuty, Duty, connect_to_db, PG_DB, database
from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError, DoesNotExist

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
    try:
        coin = Coin.get_by_id(coin_id)
        format_coin = model_to_dict(coin)
        return format_coin
    except DoesNotExist:
        return {'message': 'Resource not found'}, 404
    
@app.post('/coins')
def create_coin():
    try: 
        body = request.get_json()
        created_coin = Coin.create(name = body['name'], description = body['description'])
        return model_to_dict(created_coin), 201
    except (IntegrityError, KeyError):
        error = {'error': 'bad request',
                'message': 'bad or missing fields'}
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

    if not body:
        return {'message': 'bad request'}, 400

    allowed_fields = {'name', 'description'}
    update_data = {
        getattr(Coin, key): value
        for key, value in body.items()
        if key in allowed_fields
    }
    if not update_data:
        return {'message': 'bad request'}, 400
    
    query = Coin.update(update_data).where(Coin.id == coin_id)
    rows_updated = query.execute()

    if rows_updated == 0:
        return {'message': 'Coin not found'}, 404
    
    updated_coin = model_to_dict(Coin.get_by_id(coin_id))
    return updated_coin, 200

@app.get('/duties')
def get_all_duties():
    formatted_query = [duty for duty in Duty.select().dicts()]
    return formatted_query

@app.get('/duty/<duty_id>')
def get_duty_by_id(duty_id):
    try:
        duty = Duty.get_by_id(duty_id)
        format_duty = model_to_dict(duty)
        return format_duty
    except DoesNotExist:
        return {'message': 'Resource not found'}, 404

@app.post('/duties')
def create_duty():
    try: 
        body = request.get_json()
        created_duty = Duty.create(name = body['name'], description = body['description'])
        return model_to_dict(created_duty), 201
    except (IntegrityError, KeyError):
        error = {'error': 'bad request',
                'message': 'bad or missing fields'}
        return error, 400

@app.delete('/duty/<duty_id>')
def delete_duty_by_id(duty_id):
    delete_query = Duty.delete_by_id(duty_id)
    if(delete_query == 0):
        return {'message': 'resource not found'}, 404
    return '', 204

@app.patch('/duty/<duty_id>')
def patch_duty_by_id(duty_id):
    body = request.get_json()

    if not body:
        return {'message': 'bad request'}, 400

    allowed_fields = {'name', 'description'}
    update_data = {
        getattr(Duty, key): value
        for key, value in body.items()
        if key in allowed_fields
    }
    if not update_data:
        return {'message': 'bad request'}, 400
    
    query = Duty.update(update_data).where(Duty.id == duty_id)
    rows_updated = query.execute()

    if rows_updated == 0:
        return {'message': 'Resource not found'}, 404
    
    updated_duty = model_to_dict(Duty.get_by_id(duty_id))
    return updated_duty, 200

@app.post('/coin_duties')
def associate_coin_duty():
    try:
        body = request.get_json()
        coin_id = body['coin_id']
        duty_id = body['duty_id']
        coin = Coin.get_by_id(coin_id)
        duty = Duty.get_by_id(duty_id)
        CoinDuty.create(coin=coin, duty=duty)
        return {'message': 'Association created successfully'}, 201
    except (DoesNotExist, KeyError, IntegrityError):
        return {'message': 'bad request'}, 400
    
if __name__ == '__main__':
    app.run(debug=True)


