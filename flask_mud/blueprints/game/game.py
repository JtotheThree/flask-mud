from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user

from flask_mud.blueprints.game import events

bp = Blueprint('game', __name__, template_folder='templates')


@bp.route('/game')
@login_required
def game():
    username = current_user.username
    room = 'all'
    session['username'] = username
    session['room'] = room

    return render_template('game.html', username=username, room=room)
