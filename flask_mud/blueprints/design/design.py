from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import login_required

from flask_mud.forms.design import RoomForm
from flask_mud.models.room import Room

from flask_mud import db

bp = Blueprint('design', __name__, template_folder='templates')


@bp.route('/design', methods=['GET', 'POST'])
@login_required
def design():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(title=form.title.data, description=form.description.data)
        db.session.add(room)
        db.session.commit()
        flash('Added room: {}.'.format(form.title.data))
        return redirect(url_for('design.design'))
    return render_template('design.html', title='Design', form=form)
