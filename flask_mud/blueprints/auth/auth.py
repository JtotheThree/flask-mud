from flask import Blueprint, render_template
from flask_login import current_user, login_user, logout_user, login_required

bp = Blueprint('auth', __name__, template_folder='templates')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))