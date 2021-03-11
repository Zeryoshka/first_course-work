from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for
from flask import jsonify

from functools import wraps

import json

from app import app
from app import userSessions, users
from app import game

from app.config_module.base_config import WAITING_FOR_PLAYER, PREPARING_FOR_GAME
from app.config_module.base_config import WAITING_FOR_PLAYER__COUNTER_DOWN, WAITING_FOR_PLAYER__WAIT

def check_token(func):
	'''
	Function for decoration to check user token for correctness
	It returns function which can redirect user or render some page
	'''
	@wraps(func)
	def wrapped(*args, **kwargs):
		if not condition_truly_token():
			return redirect(url_for('index_req'))
		x = session['user_token']
		userSession = userSessions.getSessionByToken(x)
		return func(*args, **kwargs, userSession=userSession)

	return wrapped

def check_state(state):
	'''
	func for decorator for requests starts with game/...
	It needs for check user parametrs and redirect in case some problems
	It needs for checking game state for make response and redirect in case some problems
	'''
	def decor(func):
		@wraps(func)
		def wrapped(*args, **kwargs):
			if not game.state(state):
				print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
				return redirect(url_for('game_req'))
			print('================================================================')
			return func(*args, **kwargs)

		return wrapped
	
	return decor

def check_user_added_to_game(func):
	'''
	func for decorator for requests starts with game/...
	It needs for checking adding users to game for make response and redirect in case some problems
	'''
	@wraps(func)
	def wrapped(*args, **kwargs):
		if not game.userAddedToGame(kwargs['userSession']):
			return redirect(url_for('index_req'))
		return func(*args, **kwargs)

	return wrapped

@app.errorhandler(404)
def notFoundPage(error):
    return render_template('error404_template.html')

@app.route('/')
@app.route('/index')
def index_req():
	if condition_truly_token():
		userSession = userSessions.getSessionByToken(session['user_token'])
		if not game.userAddedToGame(userSession):
			game.waiting_for_player.addPlayer(userSession)
			return redirect(url_for('game_user_waiting_req'))
		return redirect(url_for('game_req'))
	return render_template('index-page_template.html')

@app.route('/game')
@check_token
@check_user_added_to_game
def game_req(userSession):
	print(game.__getattribute__("_state"))
	if game.state(WAITING_FOR_PLAYER):
		return redirect(url_for('game_user_waiting_req'))
	if game.state(PREPARING_FOR_GAME):
		print('Этого быть не должно')
		return redirect(url_for('game_preparing_req'))
	# if game.is_auction():
		# return redirect(url_for('game_user_waiting_req'))
	# if game.is_emulation():
		# return redirect(url_for('game_emaulation_req'))
	# if game.is_resaults():
		# return redirect(url_for('game_resaults_req'))
	print('Этого точно не может быть')
	return "NONE_STATE (Мы пока не знаем, как так получилось)"


@app.route('/game/user_waiting')
@check_token
@check_user_added_to_game
@check_state(WAITING_FOR_PLAYER)
def game_user_waiting_req(userSession):
	game.waiting_for_player.delPlayersWithDiedSession()
	game.waiting_for_player.start_timer()
	game.waiting_for_player.close_state()
	param = {
		'current_players_count': game.players_count,
		'need_players_count': game.needPlayersCount,
		'user_name': userSession.user.name,
		'timer_is_active': game.waiting_for_player.state(WAITING_FOR_PLAYER__COUNTER_DOWN)
	}
	return render_template('user-waiting_template.html', **param)

@app.route('/game/preparing_for_game')
@check_token
@check_user_added_to_game
@check_state(PREPARING_FOR_GAME)
def game_preparing_req(userSession):
	'''
	Functin for request "/game/preparing_for_game"
	'''
	game.preparing_for_game.start()
	param = {
		'left_time': game.preparing_for_game.left_time.seconds
	}
	return render_template('preparing-for-game_template.html',)

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
	if not condition_truly_token():
		ans = {'access': False}
	else:
		userSession = userSessions.getSessionByToken(session['user_token'])
		if not game.userAddedToGame(userSession):
			ans = {'access': False}
		else:
			game.waiting_for_player.close_state()
			ans = {
				'access': True,
				'current_players_count': game.players_count,
				'need_players_count': game.needPlayersCount,
				'timer_is_active': game.waiting_for_player.state(WAITING_FOR_PLAYER__COUNTER_DOWN)
			}
			if game.waiting_for_player.state(WAITING_FOR_PLAYER__COUNTER_DOWN):
				ans['left_time'] = game.waiting_for_player.counterDown.left_time.seconds
	return jsonify(ans)

@app.route('/game/api/check_and_close_state')
def api_check_and_close_state_req():
	if not condition_truly_token():
		ans = {'access': False}
	else:
		userSession = userSessions.getSessionByToken(session['user_token'])
		if not game.userAddedToGame(userSession):
			ans = {'access': False}
		else:
			game.waiting_for_player.close_state()
			ans = {
				'access': True,
			}

	return jsonify(ans)

def checkUserId(session):
	return (
		'user_id' in session and \
		users.existUserWithId(session['user_id']) and \
		users.getUserById(session['user_id'])
	)

def condition_truly_token():
	return ('user_token' in session) and \
	userSessions.existSessionWithToken(session['user_token']) and \
	userSessions.getSessionByToken(session['user_token']).isActive()