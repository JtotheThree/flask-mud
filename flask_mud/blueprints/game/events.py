from flask import session
from flask_socketio import emit, join_room, leave_room
from flask_mud.core.sockets import socketio

@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ': ' + message['msg']}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    print("Some shitter is leaving")
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('username') + ' has left the room.'}, room=room)