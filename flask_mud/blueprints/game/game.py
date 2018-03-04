from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('game', __name__, template_folder='templates')

@bp.route('/game')
@login_required
def game():
    return render_template('game.html')