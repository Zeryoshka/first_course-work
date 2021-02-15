from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for


from app import app
from app import userSessions, users
from app import game

@app.errorhandler(404)
def notFoundPage(error):
    return '<h1 align="center">Страница не найдена</h1>'


@app.route('/')
@app.route('/index')
def index_req():
	if checkToken(session):
		userSession = userSessions.getSessionByToken(session['user_token'])
		if game.is_waiting_for_player():
			if game.userNotAddToGame(userSession):
				game.addPlayer(userSession)
				return "Вы успешно авторизованы и добавлены к игре, игра скоро начнется" # В этом месте будет шаблон странички с ожиданием и скрипт, который будет спрашивать это
			else:
				return "Вы успешно авторизованы и добавлены к игре, игра скоро начнется. Ваш ник {0}".format(userSession.user.name) # Тут тоже
		else:
			return "Тут типо будет обратный отсчет" # render_tempates('game-wait.html')
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