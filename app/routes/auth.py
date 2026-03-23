from flask import Blueprint, jsonify, request
from app.limiter import limiter
from app.db import User
from playhouse.shortcuts import model_to_dict

users_bp = Blueprint('users', __name__)

@users_bp.post('/auth/register')
def register_user():
    body = request.get_json()
    username = body.get("username", "").strip()
    password = body.get("password", "")
    role = body.get("role", User.ROLE_USER)

    user = User(username=username, role=role)
    user.set_password(password)
    user.save(force_insert=True)
    
    user_obj = {
        "id": str(user.id),
        "username": user.username,
        "role": user.role
    }
    # return specifically this object rather than whole user object
    # avoids returning password_hash
    return user_obj, 201
