from datetime import datetime
from flask import session, jsonify, redirect
from flask_socketio import emit, join_room, leave_room
from flask_mud.core.sockets import socketio
from flask_mud.core.nlp import nlp
from random import randint
import json

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

    print("****************************** {} joined".format(username))

    user.online = True

    db.session.commit()

    emit('player_change', room=user.room_id)
    emit('refresh', room=user.room_id)


@socketio.on('client_text', namespace='/play')
def client_text(data):
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    if data['text'][0] == "/":
        if data['text'][0:5] == "/roll":
            if data["text"][6:9] == "d20":
                roll = randint(1, 20)

                category = "roll"
                content = {'dice': 'd20', 'result': str(roll)}
    else:
        category = "message"
        msg_nlp = nlp(data['text'])

        for sentence in msg_nlp.sents:
            action = [w.text for w in sentence if w.dep_ in ('xcomp', 'ccomp')]
            #who = [w for w in sentence if w.dep_ == 'nsubj']
            #obj = [w for w in sentence if w.dep_ in ('dobj')]
                
            #pobj = [w for w in action[0].children if w.dep_ == 'pobj']

            content = {'msg': data['text'], 'action': action}


    message = Message(author=username,
                      category=category,
                      content=json.dumps(content), 
                      room_id=user.room_id)

    db.session.add(message)
    db.session.commit()

    emit('refresh', room=user.room_id)


@socketio.on('left', namespace='/play')
def left(message):
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    user.online = False

    db.session.merge(user)
    db.session.commit()

    leave_room(user.room_id)

    emit('player_change', room=user.room_id)
    emit('refresh', room=user.room_id)

@socketio.on('disconnect', namespace='/play')
def disconnect():
    username = session.get('username')
    print("============================ {} left".format(username))

    user = User.query.filter_by(username=username).first()
    user.online = False

    db.session.merge(user)
    db.session.commit()

    emit('player_change', room=user.room_id)
    emit('refresh', room=user.room_id)