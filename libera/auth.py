from flask.ext.login import LoginManager

from libera.users.modesl import User

login_manager = LoginManager()

login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)
