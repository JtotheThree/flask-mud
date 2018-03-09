from flask import abort
from flask_restful import marshal_with, Resource, fields

from flask_mud.core.db import db


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    description = db.Column(db.String(512))


room_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String
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
