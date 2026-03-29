from flask import Blueprint, request
from app.auth import admin_required
from app.limiter import limiter
from app.db import Coin, Duty, CoinDuty
from app.schemas import DutyCreateSchema, DutyPatchSchema
from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError, DoesNotExist, DataError
from marshmallow import ValidationError, RAISE

duties_bp = Blueprint('duties', __name__)

duty_create_schema = DutyCreateSchema()
duty_patch_schema  = DutyPatchSchema()


def _format_duty_with_coins(duty):
    coins = Coin.select().join(CoinDuty).where(CoinDuty.duty == duty)
    return {
        'id': str(duty.id),
        'name': duty.name,
        'description': duty.description,
        'coins': [model_to_dict(c) for c in coins]
    }


@duties_bp.get('/duties')
def get_all_duties():
    return [duty for duty in Duty.select().dicts()]


@duties_bp.get('/duty/<duty_id>')
def get_duty_by_id(duty_id):
    try:
        return _format_duty_with_coins(Duty.get_by_id(duty_id))
    except (DoesNotExist, DataError):
        return {'message': 'Resource not found'}, 404


@duties_bp.get('/duty/<duty_id>/coins')
def get_coins_by_duty_id(duty_id):
    return _format_duty_with_coins(Duty.get_by_id(duty_id))


@duties_bp.get('/v2/duty/<duty_name>')
def get_duty_by_name(duty_name):
    try:
        return model_to_dict(Duty.get(Duty.name == duty_name))
    except DoesNotExist:
        return {'message': 'Resource not found'}, 404


@duties_bp.post('/duties')
@admin_required
@limiter.limit("10 per minute")
def create_duty():
    try:
        data = duty_create_schema.load(request.get_json() or {}, unknown=RAISE)
    except ValidationError as e:
        return {'message': 'bad request', 'errors': e.messages}, 400

    try:
        created_duty = Duty.create(**data)
        return model_to_dict(created_duty), 201
    except (IntegrityError, DataError):
        return {'message': 'bad request', 'errors': {'name': ['already exists or invalid']}}, 400


@duties_bp.delete('/duty/<duty_id>')
@admin_required
def delete_duty_by_id(duty_id):
    if Duty.delete_by_id(duty_id) == 0:
        return {'message': 'resource not found'}, 404
    return '', 204


@duties_bp.patch('/duty/<duty_id>')
@admin_required
def patch_duty_by_id(duty_id):
    try:
        data = duty_patch_schema.load(
            request.get_json() or {},
            partial=True,
            unknown=RAISE
        )
    except ValidationError as e:
        return {'message': 'bad request', 'errors': e.messages}, 400

    if not data:
        return {'message': 'bad request'}, 400

    update_data = {getattr(Duty, key): value for key, value in data.items()}

    try:
        rows_updated = Duty.update(update_data).where(Duty.id == duty_id).execute()
    except DataError:
        return {'message': 'Resource not found'}, 404

    if rows_updated == 0:
        return {'message': 'Resource not found'}, 404

    return model_to_dict(Duty.get_by_id(duty_id)), 200