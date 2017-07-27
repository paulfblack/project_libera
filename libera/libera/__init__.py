from .libera import app
from .auth import login_manager
from .users.views import users

app.register_blueprint(users)
