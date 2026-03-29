from flask import Blueprint, jsonify, request, session
from app.auth import current_user, set_session, login_required
from app.limiter import limiter
from app.db import User
from app.schemas import RegisterSchema, LoginSchema
from playhouse.shortcuts import IntegrityError
from marshmallow import ValidationError, RAISE

users_bp = Blueprint('users', __name__)

register_schema = RegisterSchema()
login_schema    = LoginSchema()


@users_bp.post('/auth/register')
@limiter.limit("1 per second; 5 per minute; 50 per hour")
def register_user():
    if 'role' in (request.get_json() or {}):
        return jsonify({"message": "bad request"}), 400

    try:
        data = register_schema.load(request.get_json() or {}, unknown=RAISE)
    except ValidationError as e:
        return jsonify({'message': 'bad request', 'errors': e.messages}), 400

    try:
        user = User(username=data['username'], role=User.ROLE_USER)
        user.set_password(data['password'])
        user.save(force_insert=True)
    except IntegrityError:
        return jsonify({'message': 'bad request', 'errors': {'username': ['already exists']}}), 400

    set_session(user)
    return jsonify({
        'id': str(user.id),
        'username': user.username,
        'role': user.role
    }), 201


@users_bp.post('/auth/login')
@limiter.limit("10 per minute; 50 per hour")
def login():
    try:
        data = login_schema.load(request.get_json() or {}, unknown=RAISE)
    except ValidationError as e:
        return jsonify({'message': 'bad request', 'errors': e.messages}), 400

    try:
        user = User.get(User.username == data['username'])
    except User.DoesNotExist:
        return jsonify({'message': 'invalid credentials'}), 401

    if user.is_locked:
        return jsonify({'message': 'account locked, try again later'}), 423

    if not user.check_password(data['password']):
        user.record_failed_attempt()
        return jsonify({'message': 'invalid credentials'}), 401

    set_session(user)
    user.reset_failed_attempts()
    return jsonify({
        'id': str(user.id),
        'username': user.username,
        'role': user.role
    }), 200


@users_bp.get('/auth/me')
@login_required
def me():
    user = current_user()
    return jsonify({
        'id': str(user.id),
        'username': user.username,
        'role': user.role
    }), 200


@users_bp.post('/auth/logout')
def logout():
    session.clear()
    return jsonify({'message': 'logged out'}), 200
