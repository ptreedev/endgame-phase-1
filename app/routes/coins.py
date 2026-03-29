from flask import Blueprint, request, session
from app.auth import admin_required, login_required
from app.limiter import limiter
from app.db import Coin, Duty, CoinDuty, User
from app.schemas import CoinCreateSchema, CoinPatchSchema, CoinDutySchema
from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError, DoesNotExist
from marshmallow import ValidationError, RAISE

coins_bp = Blueprint('coins', __name__)

coin_create_schema = CoinCreateSchema()
coin_patch_schema  = CoinPatchSchema()
coin_duty_schema   = CoinDutySchema()


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
@admin_required
@limiter.limit("10 per minute")
def create_coin():
    try:
        data = coin_create_schema.load(request.get_json() or {}, unknown=RAISE)
    except ValidationError as e:
        return {'message': 'bad request', 'errors': e.messages}, 400

    try:
        created_coin = Coin.create(**data)
        return model_to_dict(created_coin), 201
    except IntegrityError:
        return {'message': 'bad request', 'errors': {'name': ['already exists']}}, 400


@coins_bp.delete('/coin/<coin_id>')
@admin_required
def delete_coin_by_id(coin_id):
    if Coin.delete_by_id(coin_id) == 0:
        return {'message': 'resource not found'}, 404
    return '', 204


@coins_bp.patch('/coin/<coin_id>')
@login_required
def patch_coin_by_id(coin_id):
    try:
        data = coin_patch_schema.load(
            request.get_json() or {},
            partial=True,
            unknown=RAISE
        )
    except ValidationError as e:
        return {'message': 'bad request', 'errors': e.messages}, 400

    if not data:
        return {'message': 'bad request'}, 400

    admin_fields = {'name', 'description'}
    if set(data.keys()) & admin_fields and session.get('role') != User.ROLE_ADMIN:
        return {'message': 'forbidden'}, 403

    update_data = {getattr(Coin, key): value for key, value in data.items()}

    if Coin.update(update_data).where(Coin.id == coin_id).execute() == 0:
        return {'message': 'Coin not found'}, 404

    return model_to_dict(Coin.get_by_id(coin_id)), 200


@coins_bp.patch('/coin/<coin_id>/duties')
@admin_required
def associate_coin_duty(coin_id):
    try:
        data = coin_duty_schema.load(request.get_json() or {}, unknown=RAISE)
    except ValidationError as e:
        return {'message': 'bad request', 'errors': e.messages}, 400

    try:
        coin = Coin.get_by_id(coin_id)
        duty = Duty.get_by_id(data['duty_id'])
        CoinDuty.create(coin=coin, duty=duty)
        return {'message': 'Association created successfully'}, 200
    except (DoesNotExist, IntegrityError):
        return {'message': 'bad request'}, 400