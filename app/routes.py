from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for
from flask import jsonify
from flask import make_response

from functools import wraps

import json

from app import app
from app import userSessions, users
from app import game

from app.config_module.base_config import WAITING_FOR_PLAYER, PREPARING_FOR_GAME, AUCTION, EMULATION
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
                return redirect(url_for('game_req'))
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
            if game.waiting_for_player.needMorePlayer():
                game.waiting_for_player.addPlayer(userSession)
                return redirect(url_for('game_user_waiting_req'))
            return 'Извините, но игроков слишком много'
        return redirect(url_for('game_req'))
    return render_template('index-page_template.html')


@app.route('/game')
@check_token
@check_user_added_to_game
def game_req(userSession):
    if game.state(WAITING_FOR_PLAYER):
        return redirect(url_for('game_user_waiting_req'))
    if game.state(PREPARING_FOR_GAME):
        return redirect(url_for('game_preparing_req'))
    if game.state(AUCTION):
        return redirect(url_for('game_auction_req'))
    if game.state(EMULATION):
        return redirect(url_for('game_emulation_req'))
    return "NONE_STATE (Мы пока не знаем, как так получилось)"


@app.route('/game/user_waiting')
@check_token
@check_user_added_to_game
@check_state(WAITING_FOR_PLAYER)
def game_user_waiting_req(userSession):
    game.waiting_for_player.delPlayersWithDiedSession()
    game.waiting_for_player.start_timer()
    if game.waiting_for_player.close_state():
        return redirect(url_for('game_req'))
    param = {
        'current_players_count': game.players.players_count,
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
    if game.preparing_for_game.close_state():
        return redirect(url_for('game_req'))
    param = {
        'left_time': game.preparing_for_game.counterDown.left_time.seconds,
        'prediction_file': game.weathercast_file,
        'lots_file': game.lots_file
    }
    return render_template('preparing-for-game_template.html', **param)

# Заглушка, пока Илья не сделает
class Lot:
    def __init__(self, mini, maxi, name, id, who_bought, is_current, purchase_cost):
        self.max_cost = maxi
        self.min_cost = mini
        self.who_bought = who_bought
        self.name = name
        self.id = id
        self.is_current = is_current
        self.purchase_cost = purchase_cost



@app.route('/game/auction')
@check_token
@check_user_added_to_game
@check_state(AUCTION)
def game_auction_req(userSession):
    '''
    Functin for request "/game/auction"
    '''
    game.auction.start()
    param = {
        'user': userSession.user,
        'lots': game.auction.actual_lots,
        'cur_lot': game.auction.cur_lot,
        'left_time': game.auction.bid_counter_down.left_time.seconds,
        'have_bid': game.auction.cur_lot.user_have_bid(userSession.user)
    }
    if param['have_bid']:
        param['my_bid'] = game.auction.cur_lot.get_user_bid(userSession.user)

    resp = make_response(render_template('auction_template.html', **param))
    resp.set_cookie('left_time', str(game.auction.bid_counter_down.left_time.seconds), 100)
    resp.set_cookie('user_id', str(userSession.user.id),)
    resp.set_cookie('user_name', str(userSession.user.name))
    resp.set_cookie('cur_lot_id', str(game.auction.cur_lot.id), path='/game/auction')

    return resp

@app.route('/game/emulation')
@check_token
@check_user_added_to_game
@check_state(EMULATION)
def game_emulation_req(userSession):
    '''
    Functin for request "/game/emulation"
    '''
    game.emulation.start()
    param = {
        'user': userSession.user,
        'cur_result': game.emulation.cur_result
    }
    resp = make_response(render_template('emulation_template.html', **param))
    
    return resp


@app.route('/authorization')
def authorization_req():
    if checkUserId(session):
        session['user_token'] = userSessions.addUserSesion(
            users.getUserById(session['user_id']))
        return redirect(url_for('index_req'))
    return redirect(url_for('registration_req'))


@app.route('/registration')
def registration_req():
    session['user_id'] = users.addUser()
    return redirect(url_for('authorization_req'))

@app.route('/game/api/make_bid', methods=['POST'])
@check_token
@check_user_added_to_game
@check_state(AUCTION)
def api_make_bid_req(userSession):
    '''
    Functin for request "/game/api/make_bid"
    '''
    game.auction.start()
    req = dict(request.form)
    is_successful, message = game.auction.make_bid(userSession.user, int(req['lot_id']), float(req['price']))
    resp = {
        'is_successful': is_successful,
        'message': message
    }
    return jsonify(resp)


@app.route('/game/api/update_lots')
@check_token
@check_user_added_to_game
@check_state(AUCTION)
def api_update_lots_req(userSession):
    '''
    Functin for request "/game/api/update_lots"
    '''
    game.auction.start()
    game.auction.check_change_lot()
    if not game.state(AUCTION):
        resp = {
            'is_auction': False
        }
        return resp
    resp = {
        'is_auction': True,
        'user_id': userSession.user.id,
        'lots': game.auction.export_data(),
        'cur_lot': game.auction.cur_lot.return_info(),
        'left_time': game.auction.bid_counter_down.left_time.seconds
    }
    return jsonify(resp)



@app.route('/game/api/check_for_waiting')
def api_check_for_waiting_req():
    if not condition_truly_token():
        ans = {'access': False}
    else:
        userSession = userSessions.getSessionByToken(session['user_token'])
        if not game.userAddedToGame(userSession):
            ans = {'access': False}
        else:
            ans = {
                'access': True,
                'current_players_count': game.players.players_count,
                'need_players_count': game.needPlayersCount,
                'timer_is_active': game.waiting_for_player.state(WAITING_FOR_PLAYER__COUNTER_DOWN),
                'state_closed': game.waiting_for_player.close_state()
            }
            if game.waiting_for_player.state(WAITING_FOR_PLAYER__COUNTER_DOWN):
                ans['left_time'] = game.waiting_for_player.counterDown.left_time.seconds
    return jsonify(ans)


@app.route('/game/api/check_for_preparing')
def api_check_for_preparing_req():
    if not condition_truly_token():
        ans = {'access': False}
    else:
        userSession = userSessions.getSessionByToken(session['user_token'])
        if not game.userAddedToGame(userSession):
            ans = {'access': False}
        else:
            ans = {
                'access': True,
                'state_closed': game.preparing_for_game.close_state()
            }

    return jsonify(ans)


def checkUserId(session):
    return (
        'user_id' in session and
        users.existUserWithId(session['user_id']) and
        users.getUserById(session['user_id'])
    )


def condition_truly_token():
    return ('user_token' in session) and \
        userSessions.existSessionWithToken(session['user_token']) and \
        userSessions.getSessionByToken(session['user_token']).isActive()
