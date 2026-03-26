from functools import wraps

from flask import session

def set_session(user) -> None:
    session.clear()
    session['user_id'] = str(user.id)
    session['role'] = user.role


def current_user():
    from app.db import User
    uid = session.get('user_id')
    if uid is None:
        return None
    try:
        return User.get_by_id(uid)
    except Exception:
        session.clear()
        return None
    
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return {'message': 'unauthorised'}, 401
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return {'message': 'unauthorised'}, 401
        if session.get('role') != 'admin':
            return {'message': 'forbidden'}, 403
        return f(*args, **kwargs)
    return decorated