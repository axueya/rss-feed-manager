from flask import Flask, redirect, render_template, jsonify
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis

from app import api_bp
from blacklist import BLACKLIST
from models import db, redis_cache
from flask_docs import ApiDoc

app = Flask(__name__)

ApiDoc(app)

jwt = JWTManager(app)  # /auth


# Adding claims
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


# Returns if token is in blacklist or not
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification Failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    })


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    })


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    })


def create_app(config_filename):
    app.config.from_pyfile(config_filename)
    app.register_blueprint(api_bp, url_prefix='/api/v1.0')
    db.init_app(app)
    redis_cache.init_app(app)
    return app


if __name__ == "__main__":
    app = create_app('config_local.py')

    app.run(host='0.0.0.0', debug=True)
