from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required

bp = Blueprint('user', __name__, template_folder='templates')

@bp.route('/characters')
@login_required
def characters():
    return render_template('characters.html')