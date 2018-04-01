from datetime import datetime
from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
import json

from flask_mud.blueprints.play import events
from flask_mud.models.user import User
from flask_mud.models.room import Room
from flask_mud.forms.rooms import RoomsForm, CreateRoomForm

from flask_mud import db

bp = Blueprint('play', __name__, template_folder='templates')


@bp.route('/play')
@login_required
def play():
    username = current_user.username
    session['username'] = username
    session['in_room'] = True

    user = User.query.filter_by(username=username).first()

    if not user.room_id:
        return redirect(url_for('play.rooms'))
    else:
        room = Room.query.filter_by(id=user.room_id).first()

        return render_template('play.html', title=room.title,
            username=username, room=room)


@bp.route('/rooms', methods=['GET', 'POST'])
@login_required
def rooms():
    form = RoomsForm()

    if form.validate_on_submit():
        room = Room.query.filter_by(id=int(form.room_list.data)).first()

        if room is None:
            flash("Error: cannot locate room")
            return redirect(url_for('play.play'))

        if room.password_required and not room.check_password(form.password.data):
            flash('Invalid password')
            return redirect(url_for('play.play'))

        user = User.query.filter_by(username=current_user.username).first()
        user.room_id = room.id

        room = Room.query.filter_by(id=room.id).first()
        room.add_player(user)

        db.session.commit()

        return redirect(url_for('play.play'))

    return render_template('rooms.html', form=form)

@bp.route('/create_room', methods=['GET', 'POST'])
@login_required
def create_room():
    form = CreateRoomForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        password_required = form.password_required.data

        room = Room(title=title, description=description, 
                    password_required=password_required)

        if password_required:
            room.set_password(form.password.data)

        db.session.add(room)
        db.session.commit()
        flash('You have created a new room.')
        return redirect(url_for('play.play'))

    return render_template('create_room.html', form=form)

@bp.route('/leave_room')
@login_required
def leave_room():
    user = User.query.filter_by(username=current_user.username).first()

    room = Room.query.filter_by(id=user.room_id).first()
    room.remove_player(user)

    user.room_id = None

    db.session.commit()

    return redirect(url_for('main.index'))

@bp.route('/messages')
@login_required
def messages():
    user = User.query.filter_by(username=current_user.username).first()
    room = Room.query.filter_by(id=user.room_id).first()
    messages = list(room.messages())

    for message in messages:
        message.content = json.loads(message.content)

    return render_template('messages.html', messages=messages)

@bp.route('/get_players')
@login_required
def get_players():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(id=user.room_id).first()

    players = room.get_players()

    return render_template('player_list.html', players=players)
    #user = user.query.filter_by(username=current_user.username).first()