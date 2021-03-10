from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for
from flask import jsonify

import json

from app import app
from app import userSessions, users
from app import game

from app.config_module.base_config import COUNT_DOWN_BEFORE_PREPARING__TIME
from app.config_module.base_config import COUNT_DOWN_BEFORE_PREPARING, WAITING_FOR_PLAYER

@app.errorhandler(404)
def notFoundPage(error):
    return render_template('error404_template.html')

@app.route('/')
@app.route('/index')
def index_req():
	if checkToken(session):
		userSession = userSessions.getSessionByToken(session['user_token'])
		if not game.userAddedToGame(userSession):
			game.addPlayer(userSession)
			return redirect(url_for('game_user_waiting_req'))
		# return "Вы успешно авторизованы и добавлены к игре, игра скоро начнется. Ваш ник {0}".format(userSession.user.name) # Тут тоже
		# return "Тут типо будет обратный отсчет" # render_tempates('game-wait.html')
	return render_template('index-page_template.html')

@app.route('/game')
def game_req():
	if checkToken(session):
		userSession = userSessions.getSessionByToken(session['user_token'])
		if game.userAddedToGame(userSession):
			if game.state(WATITNG_FOR_PLAYER):
				return redirect(url_for('game_user_waiting_req'))
			if game.is_preparing_for_game():
				return redirect(url_for('game_preparing_req'))
			if game.is_auction():
				return redirect(url_for('game_user_waiting_req'))
			if game.is_emulation():
				return redirect(url_for('game_emaulation_req'))
			if game.is_resaults():
				return redirect(url_for('game_resaults_req'))
			return "NONE_STATE (Мы пока не знаем, как так получилось)"
	return redirect(url_for('index_req'))


@app.route('/game/user_waiting')
def game_user_waiting_req():
	if not checkToken(session):
		return redirect(url_for('index_req'))
	userSession = userSessions.getSessionByToken(session['user_token'])
	if not game.userAddedToGame(userSession):
		return redirect(url_for('index_req'))
	if not game.state(COUNT_DOWN_BEFORE_PREPARING) and not game.state(WATITNG_FOR_PLAYER):
		return redirect(url_for('game_req'))
	game.state_to_count_down_before_preparing()
	param = {
		'current_players_count': game.get_players_count(),
		'need_players_count': game.needPlayersCount,
		'user_name': userSession.user.name,
	}
	return render_template('user-waiting_template.html', **param)


@app.route('/authorization')
def authorization_req():
	if checkUserId(session):
		session['user_token'] = userSessions.addUserSesion(users.getUserById(session['user_id']))
		return redirect(url_for('index_req'))
	else:
		return redirect(url_for('registration_req'))


@app.route('/registration')
def registration_req():
	session['user_id'] = users.addUser()
	return redirect(url_for('authorization_req'))

@app.route('/game/api/check_for_waiting')
def api_check_for_waiting_req():
	if not checkToken(session):
		return redirect(url_for('index_req'))
	userSession = userSessions.getSessionByToken(session['user_token'])
	if not game.userAddedToGame(userSession):
		return redirect(url_for('index_req'))
	ans = {
			'current_players_count': game.get_players_count(),
			'need_players_count': game.needPlayersCount,
			'is_count_down_before_preparing': game.state(COUNT_DOWN_BEFORE_PREPARING)
	}
	if game.state(COUNT_DOWN_BEFORE_PREPARING):
		ans['left_time'] = (COUNT_DOWN_BEFORE_PREPARING__TIME - game.count_down_1_active_time).seconds
	return jsonify(ans)

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