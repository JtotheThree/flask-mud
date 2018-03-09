from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
from flask_login import UserMixin
from flask_restful import marshal_with, Resource, fields

from flask_mud.core.db import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    created = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'created': fields.DateTime,
    'role': fields.Integer,
}


class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = User.query.filter(User.id == id).first()

        if not user:
            abort(404, message="User {} doesn't exist.".format(id))
        return user


class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users
