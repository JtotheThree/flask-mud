from datetime import datetime
from flask import session
from flask_socketio import emit, join_room, leave_room
from flask_mud.core.sockets import socketio

class Message(object):
    def __init__(self, username, timestamp, message):
        self.username = username
        self.timestamp = timestamp
        self.message = message

@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') +
                    ' has entered the room.'}, room=room)


@socketio.on('message', namespace='/chat')
def text(message):
    room = session.get('room')

    msg = Message(session.get('username'), datetime.now(), message['msg'])

    if 'messages' not in session:
        session['messages'] = list()
        session['messages'].append(msg)

    print(session['messages'])

    emit('message', {'msg': session.get('username') +
                     ': ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    print("left")
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('username') +
                    ' has left the room.'}, room=room)
