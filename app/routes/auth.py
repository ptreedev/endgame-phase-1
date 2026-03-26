from flask import Blueprint, jsonify, request
from app.auth import current_user, set_session
from app.limiter import limiter
from app.db import User
from playhouse.shortcuts import IntegrityError

users_bp = Blueprint('users', __name__)

@users_bp.post('/auth/register')
def register_user():
    body = request.get_json()
    username = body.get("username", "").strip()
    password = body.get("password", "")
    role = body.get("role", User.ROLE_USER)

    if not username or not password:
        return jsonify({"message": "bad request"}), 400
    
    if role not in User.ROLES:
        return jsonify({"message": "bad request"}), 400

    try:
        user = User(username=username, role=role)
        user.set_password(password)
        user.save(force_insert=True)
    except IntegrityError:
        return jsonify({"message": "bad request"}), 400
    
    set_session(user)
    # return specifically this object rather than whole user object
    # avoids returning password_hash
    user_obj = {
        "id": str(user.id),
        "username": user.username,
        "role": user.role
    }

    return user_obj, 201

@users_bp.post('/auth/login')
def login():
    body = request.get_json() or {}
    username = body.get("username", "").strip()
    password = body.get("password", "")

    if not username or not password:
        return jsonify({"message": "bad request"}), 400

    try:
        user = User.get(User.username == username)
    except User.DoesNotExist:
        return jsonify({"message": "invalid credentials"}), 401


    if not user.check_password(password):
        return jsonify({"message": "invalid credentials"}), 401
    
    user_obj = {
        'id': str(user.id),
        'username': user.username,
        'role': user.role
    }
    set_session(user)

    return user_obj, 200 


@users_bp.get('/auth/me')
def me():
    user = current_user()
    return jsonify({
        "id": str(user.id),
        "username": user.username,
        "role": user.role
    }), 200    