from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

# FONT HACK
@bp.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('static/fonts', path)