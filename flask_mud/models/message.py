from datetime import datetime
from flask_restful import marshal_with, Resource, fields

from flask_mud.core.db import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.String(1024))

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


message_fields = {
    'id': fields.Integer,
    'author': fields.String,
    'timestamp': fields.DateTime,
    'content': fields.String,
    'room_id': fields.Integer,
}


class MessageResource(Resource):
    @marshal_with(message_fields)
    def get(self, id):
        message = Message.query.filter(Message.id == id).first()

        if not message:
            abort(404, message="Message {} doesn't exist.".format(id))
        return message


class MessageListResource(Resource):
    @marshal_with(message_fields)
    def get(self):
        messages = Message.query.all()
        return messages