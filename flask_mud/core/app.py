import os
import datetime
from flask import Flask
from flask_migrate import Migrate

from flask_mud import db
from flask_mud.core.login import login_manager
from flask_mud.core.moment import moment
from flask_mud.core.api import api
from flask_mud.core.cli import gulp_command
from flask_mud.core.sockets import socketio
from flask_mud.core.filters import markdown_filter

from config import Config


def create_app():
    app = Flask('flask_mud')

    load_config(app)
    setup_db(app)
    setup_models(app)
    setup_extensions(app)
    setup_cli(app)
    register_handlers(app)
    register_blueprints(app)
    register_resources(app)
    register_filters(app)

    return app


def load_config(app):
    app.config.from_object(Config)
    # app.config.from_pyfile('../instance/config.cfg')

    if not app.config['ASSETS_FOLDER']:
        app.config['ASSETS_FOLDER'] = os.path.join(
            app.root_path, 'static', 'assets')


def setup_db(app):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

    db.init_app(app)


def setup_models(app):
    import flask_mud.models.user
    import flask_mud.models.room
    import flask_mud.models.message

    migrate = Migrate(app, db)


def setup_extensions(app):
    login_manager.init_app(app)
    moment.init_app(app)
    socketio.init_app(app)


def setup_cli(app):
    app.cli.command('gulp')(gulp_command)


def register_handlers(app):
    @app.shell_context_processor
    def extend_shell_context():
        ctx = {'db': db}
        ctx.update(db.Model._decl_class_registry)
        ctx.update((x, getattr(datetime, x))
                   for x in ('date', 'time', 'datetime', 'timedelta'))
        return ctx


def register_blueprints(app):
    from flask_mud.blueprints.main.main import bp as main_bp
    from flask_mud.blueprints.auth.auth import bp as auth_bp
    from flask_mud.blueprints.play.play import bp as play_bp
    from flask_mud.blueprints.user.user import bp as user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(play_bp)
    app.register_blueprint(user_bp)

def register_resources(app):
    from flask_mud.models.user import UserResource, UserListResource
    from flask_mud.models.room import RoomResource, RoomListResource
    from flask_mud.models.message import MessageResource, MessageListResource

    api.add_resource(UserResource, '/api/user/<string:id>', endpoint='user')
    api.add_resource(UserListResource, '/api/users')
    api.add_resource(RoomResource, '/api/room/<string:id>', endpoint='room')
    api.add_resource(RoomListResource, '/api/rooms')
    api.add_resource(MessageResource, '/api/message/<string:id>', endpoint='message')
    api.add_resource(MessageListResource, '/api/messages')

    api.init_app(app)

def register_filters(app):
    app.jinja_env.filters['markdown'] = markdown_filter