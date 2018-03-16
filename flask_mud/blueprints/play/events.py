from datetime import datetime
from flask import session, jsonify, redirect
from flask_socketio import emit, join_room, leave_room
from flask_mud.core.sockets import socketio

from flask_mud.models.user import User
from flask_mud.models.room import Room
from flask_mud.models.message import Message

from flask_mud.core.db import db


@socketio.on('client_connected', namespace='/play')
def client_connected(data):
    username = session.get('username')

    user = User.query.filter_by(username=username).first()

    if not user.room_id:
        return

    join_room(user.room_id)

    emit('refresh', room=user.room_id)


@socketio.on('client_text', namespace='/play')
def client_text(data):
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    if data['text'][0] == "/":
        print(data['text'])
    else:
        message = Message(author=username, 
                          content=data['text'], 
                          room_id=user.room_id)

        db.session.add(message)
        db.session.commit()

    emit('refresh', room=user.room_id)


@socketio.on('left', namespace='/play')
def left(message):
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    leave_room(user.room_id)