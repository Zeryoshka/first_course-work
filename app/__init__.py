#import os
#import jinja2
from flask import Flask

from app.config_module.base_config import SECRET_KEY
from app.sessions_module.userSessions import UserSessions
from app.users_module.users import Users
from app.game_module.game import Game

#from flask import render_template

# template_dir = os.path.join(os.path.dirname(__file__), 'templates' ) # Убрать 'templates' в конфиги
# jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


app = Flask(__name__)
app.secret_key = SECRET_KEY
userSessions = UserSessions()
users = Users()
game = Game()

from app import routes
