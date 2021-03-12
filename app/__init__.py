from flask import Flask

from app.config_module.base_config import SECRET_KEY, STATIC_FOLDER, TEMPLATE_FOLDER
from app.game_module.game import Game
from app.users_module.users import Users
from app.sessions_module.userSessions import UserSessions

app = Flask(__name__)

app.secret_key = SECRET_KEY
app.static_folder = STATIC_FOLDER
app.template_folder = TEMPLATE_FOLDER

userSessions = UserSessions()
users = Users()
game = Game()

from app import routes
