from flask import render_template
from flask import request

from app import app


@app.errorhandler(404)
def notFoundPage(error):
    return '<h1 align="center">Страница не найдена</h1>'


@app.route('/')
@app.route('/index')
def index():
	return render_template('lobby/lobby.html')


@app.route('/registration', methods=['GET','POST'])
def register_req():
	if request.method == 'GET':
		return render_template('registration/registration.html')
	elif request.method == 'POST':
		return render_template('registration/registration.html')


@app.route('/authorization')
def authorization_req():
	return render_template('authorization/authorization.html')




@app.route('/auction')
def auction_req():
	return "Страничка с аукционами"

