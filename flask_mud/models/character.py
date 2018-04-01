from datetime import datetime
from flask_restful import marshal_with, Resource, fields

from flask_mud.core.db import db

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, default=datetime.now())

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    name = db.Column(db.String(32))
    race = db.Column(db.String(32))
    char_class = db.Column(db.String(32))
    alignment = db.Column(db.String(32))
    xp = db.Column(db.Integer, default=0)
    max_hitpoints = db.Column(db.Integer)
    current_hitpoints = db.Column(db.Integer)

    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)