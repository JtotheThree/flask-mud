from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')