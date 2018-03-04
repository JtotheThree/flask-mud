import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import find_modules, import_string

from flask_mud import db
from flask_mud.core.login import login_manager
from flask_mud.util.db import import_all_models

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask('flask_mud')
    app.config.from_object(Config)
    app.config.from_pyfile('../instance/config.cfg')

    register_blueprints(app)
    setup_db(app)
    setup_extensions(app)

    return app


def setup_db(app):
    import flask_mud.models.user

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

    db.init_app(app)


def setup_extensions(app):
    login_manager.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    from flask_mud.views.home import bp as home_bp

    app.register_blueprint(home_bp)