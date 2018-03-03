from flask import render_template

from flask_mud.blueprints.main import bp

@bp.route('/')
def index():
    return "Hello, world!"
