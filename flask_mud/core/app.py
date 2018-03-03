from flask import Flask
import os

from flask_mud import db
from flask_mud.config import configs
from flask_mud.core.login import login_manager
from flask_mud.core.sockets import socketio


def create_app():
    app = Flask(__name__)
    load_config(app)
    setup_db(app)
    setup_extensions(app)
    register_handlers(app)
    register_blueprints(app)

    return app


def load_config(app):
    env = os.environ.get('FLASK_ENV', 'dev')
    app.config.from_object(configs[env])


def setup_db(app):
    db.init_app(app)


def setup_extensions(app):
    login_manager.init_app(app)
    socketio.init_app(app)


def register_handlers(app):
    @app.shell_context_processor
    def _extend_shell_context():
        ctx = {'db': db}
        return ctx


def register_blueprints(app):
    from flask_mud.blueprints import main_bp, user_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
