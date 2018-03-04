from flask_login import LoginManager

from flask_mud.models.user import User
from flask_mud import db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if not user:
        return None
    return user