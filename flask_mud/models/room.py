from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
from flask_restful import marshal_with, Resource, fields

from flask_mud.models.message import Message

from flask_mud.core.db import db

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    description = db.Column(db.String(512))
    password_hash = db.Column(db.String(128))
    password_required = db.Column(db.Boolean)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    last_played = db.Column(db.DateTime, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    messages = db.relationship('Message', backref='room', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def messages(self):
        messages = Message.query.filter_by(room_id=self.id)
        return messages.order_by(Message.timestamp.asc())

room_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'created': fields.DateTime,
    'last_played': fields.DateTime,
}


class RoomResource(Resource):
    @marshal_with(room_fields)
    def get(self, id):
        room = Room.query.filter(Room.id == id).first()

        if not room:
            abort(404, message="Room {} doesn't exist.".format(id))
        return room


class RoomListResource(Resource):
    @marshal_with(room_fields)
    def get(self):
        rooms = Room.query.all()
        return rooms