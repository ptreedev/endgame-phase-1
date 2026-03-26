from flask import Blueprint
from app.auth import admin_required
from app.db import RequestLog
from playhouse.shortcuts import model_to_dict

logs_bp = Blueprint('logs', __name__)


@logs_bp.get('/requests')
@admin_required
def get_requests():
    logs = RequestLog.select().order_by(RequestLog.timestamp.desc()).limit(100)
    return [model_to_dict(log) for log in logs]