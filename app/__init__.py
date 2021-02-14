import os
import jinja2
from flask import Flask
from flask import render_template

template_dir = os.path.join(os.path.dirname(__file__), 'templates' ) # Убрать 'templates' в конфиги
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


app = Flask(__name__)

from app import routes

"""
from flask import Flask

app = Flask(__name__)

from app import routes
"""