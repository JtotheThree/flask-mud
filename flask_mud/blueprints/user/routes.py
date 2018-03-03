from flask import render_template

from flask_mud.blueprints.user import bp

@bp.route('/user')
def user_page():
    return "Hello, world!"
