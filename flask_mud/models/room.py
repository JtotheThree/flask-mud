from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
from flask_restful import marshal_with, Resource, fields

from flask_mud.models.message import Message

from flask_mud.core.db import db

players = db.Table('players',
    db.Column('room_id', db.Integer, db.ForeignKey('room.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

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

    playing = db.relationship('User', secondary=players,
        primaryjoin=(players.c.room_id == id),
        backref=db.backref('players', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def messages(self):
        messages = Message.query.filter_by(room_id=self.id)
        return messages.order_by(Message.timestamp.asc())

    def add_player(self, user):
        if not self.is_playing(user):
            self.playing.append(user)

    def remove_player(self, user):
        if self.is_playing(user):
            self.playing.remove(user)

    def is_playing(self, user):
        from flask_mud.models.user import User
        return self.playing.filter((players.c.room_id == self.id) & (players.c.user_id == user.id)).count() > 0

    def get_players(self):
        from flask_mud.models.user import User
        return User.query.join(players).join(Room).filter((players.c.user_id == User.id) & (players.c.room_id == Room.id)).all()


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