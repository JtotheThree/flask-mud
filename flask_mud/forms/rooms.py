from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms_html5 import AutoAttrMeta

from flask_mud.models.room import Room

class RoomsForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass
        
    room_list = SelectField('Room List')
    password = PasswordField('Password')
    submit = SubmitField('Join Room')

    def __init__(self, **kwargs):
        super(RoomsForm, self).__init__(**kwargs)
        self.room_list.choices = self.get_rooms()

    def get_rooms(self):
        choices = [(str(row.id), row.title) for row in Room.query.all()]
        return choices

class CreateRoomForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    password = PasswordField('Password')
    password_required = BooleanField('Password Required')
    submit = SubmitField('Create Room')