from flask import Blueprint, request
from app.limiter import limiter
from app.db import Coin, Duty, CoinDuty
from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError, DoesNotExist

coins_bp = Blueprint('coins', __name__)

@coins_bp.get('/coins')
def get_all_coins():
    result = []
    for coin in Coin.select():
        coin_dict = model_to_dict(coin)
        duties = Duty.select().join(CoinDuty).where(CoinDuty.coin == coin)
        coin_dict['duties'] = [model_to_dict(d) for d in duties]
        result.append(coin_dict)
    return result

@coins_bp.get('/coin/<coin_id>')
def get_coin_by_id(coin_id):
    try:
        return model_to_dict(Coin.get_by_id(coin_id))
    except DoesNotExist:
        return {'message': 'Resource not found'}, 404
    
@coins_bp.post('/coins')
@limiter.limit("10 per minute")
def create_coin():
    try:
        body = request.get_json()
        created_coin = Coin.create(name=body['name'], description=body['description'])
        return model_to_dict(created_coin), 201
    except (IntegrityError, KeyError):
        return {'error': 'bad request', 'message': 'bad or missing fields'}, 400

@coins_bp.delete('/coin/<coin_id>')
def delete_coin_by_id(coin_id):
    if Coin.delete_by_id(coin_id) == 0:
        return {'message': 'resource not found'}, 404
    return '', 204

@coins_bp.patch('/coin/<coin_id>')
def patch_coin_by_id(coin_id):
    body = request.get_json()
    if not body:
        return {'message': 'bad request'}, 400

    allowed_fields = {'name', 'description', 'complete'}
    update_data = {
        getattr(Coin, key): value
        for key, value in body.items()
        if key in allowed_fields
    }
    if not update_data:
        return {'message': 'bad request'}, 400

    if Coin.update(update_data).where(Coin.id == coin_id).execute() == 0:
        return {'message': 'Coin not found'}, 404

    return model_to_dict(Coin.get_by_id(coin_id)), 200

@coins_bp.patch('/coin/<coin_id>/duties')
def associate_coin_duty(coin_id):
    try:
        body = request.get_json()
        coin = Coin.get_by_id(coin_id)
        duty = Duty.get_by_id(body['duty_id'])
        CoinDuty.create(coin=coin, duty=duty)
        return {'message': 'Association created successfully'}, 200
    except (DoesNotExist, KeyError, IntegrityError):
        return {'message': 'bad request'}, 400    