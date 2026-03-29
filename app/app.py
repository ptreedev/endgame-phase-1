from datetime import datetime
from flask import Flask, request, g
from flask_cors import CORS
from app.db import *
from app.limiter import limiter
from app.routes.logs import logs_bp
from app.routes.coins import coins_bp
from app.routes.duties import duties_bp
from app.routes.auth import users_bp
import os

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
limiter.init_app(app)
CORS(app, origins=[os.getenv('CORS_ORIGIN'), os.getenv('DEV_CORS_ORIGIN')], supports_credentials=True)

app.register_blueprint(logs_bp)
app.register_blueprint(coins_bp)
app.register_blueprint(duties_bp)
app.register_blueprint(users_bp)

@app.before_request
def _db_connect():
    if not app.testing:
        connect_to_db(app)

@app.teardown_request
def _db_close(exc):
    if not app.testing and not database.is_closed():
        database.close()

@app.before_request
def log_request():
    g.start_time = datetime.now()

@app.after_request
def log_response(response):
    if request.path != '/requests':
        RequestLog.create(
            method=request.method,
            path=request.path,
            timestamp=g.start_time,
            status_code=response.status_code
        )
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
    # app.run(debug=True)


