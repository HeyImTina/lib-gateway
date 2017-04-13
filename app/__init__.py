# coding:utf-8
from flask import Flask
from flask_redis import FlaskRedis

from app.api_1_0 import api
from app.model import db
from app.model.user import login_manager
from config import config

redis_store = FlaskRedis()


def create_app(config_name=None):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config[config_name])

    db.init_app(flask_app)
    redis_store.init_app(flask_app)
    login_manager.init_app(flask_app)

    flask_app.register_blueprint(api, url_prefix="/api/v1.0")

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run()
