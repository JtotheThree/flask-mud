from flask_login import LoginManager

from flask_mud.models import user

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if not user or user.is_deleted:
        return None
    return user