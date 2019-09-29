from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.main.config import config_by_name

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    if (config_name == 'dev'):
        app.config.from_pyfile('application.cfg', silent=True)

    db.init_app(app)

    return app
