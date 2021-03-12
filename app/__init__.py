#import os
#import jinja2
from app import routes
from flask import Flask

from app.config_module.base_config import SECRET_KEY, STATIC_FOLDER, TEMPLATE_FOLDER
from app.sessions_module.userSessions import UserSessions
from app.users_module.users import Users
from app.game_module.game import Game

#from flask import render_template

# template_dir = os.path.join(os.path.dirname(__file__), 'templates' ) # Убрать 'templates' в конфиги
# jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


app = Flask(__name__)

app.secret_key = SECRET_KEY
app.static_folder = STATIC_FOLDER
app.template_folder = TEMPLATE_FOLDER

userSessions = UserSessions()
users = Users()
game = Game()
