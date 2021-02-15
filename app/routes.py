from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for


from app import app
from app import userSessions
from app import users

@app.errorhandler(404)
def notFoundPage(error):
    return '<h1 align="center">Страница не найдена</h1>'


@app.route('/')
@app.route('/index')
def index_req():
	if checkToken(session):
		return "Вы успешно авторизованы, игра скоро начнется"
	else:
		return redirect(url_for('registration_req'))

@app.route('/authorization')
def authorization_req():
	if checkUserId(session):
		session['user_token'] = userSessions.addUserSesion(users.getUserById(session['user_id']))
		return redirect(url_for('index_req'))
	else:
		return redirect(url_for('registration_req'))


@app.route('/registartion')
def registration_req():
	session['user_id'] = users.addUser()
	return redirect(url_for('authorization_req'))


def checkToken(session):
	return (
		'user_token' in session and \
		userSessions.existSessionWithToken(session['user_token']) and \
		userSessions.getSessionByToken(session['user_token']).isActive()
	)

def checkUserId(session):
	return (
		'user_id' in session and \
		users.existUserWithId(session['user_id']) and \
		users.getUserById(session['user_id'])
	)