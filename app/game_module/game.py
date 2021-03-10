from app.game_module.player import Player
from .counter_down import CounterDown

from app.config_module.base_config import NONE_STATE, WAITING_FOR_PLAYER, PREPARING_FOR_GAME, \
	AUCTION, EMULATION, RESULTS, COUNT_DOWN_BEFORE_PREPARING

from app.config_module.base_config import WAITING_FOR_PLAYER__COUNTER_DOWN, WAITING_FOR_PLAYER__WAIT

from app.config_module.base_config import COUNT_DOWN_BEFORE_PREPARING__TIME

from datetime import datetime, timedelta

_states = [WATITNG_FOR_PLAYER, PREPARING_FOR_GAME, AUCTION, EMULATION, RESULTS]

class Game():
	'''
	Class for game object
	'''
	def __init__(self):
		self._state = WATITNG_FOR_PLAYER
		self.needPlayersCount = 3
		self._players = []
		self.waiting_for_player = Waiting_for_player(self)

	def state(self, state):
		return self._state == state

	def userAddedToGame(self, userSession):
		for player in self._players:
			if player.userSession == userSession:
				return True
		return False

	@property
	def players_count(self):
		return len(self._players)


class Waiting_for_player:
	def __init__(self, game):
		self.game = game
		self.sub_state = WAITING_FOR_PLAYER__WAIT
		self.counterDown = CounterDown(COUNT_DOWN_BEFORE_PREPARING__TIME)

	def addPlayer(self, userSession):
		self.game.append(Player(userSession))

	def start_timer(self):
		if (len(self.game._players) == self.game.needPlayersCount):
			self.counterDown.start()
		return self.counterDown.started

	def __getattribute__(self, name):
		self.delPlayersWithDiedSession()
		assert(self.game.state(WAITING_FOR_PLAYER))
		assert(len(self.game._players) <= self.game.needPlayersCount)
		return super().__getattribute__(self, name)

	def delPlayersWithDiedSession(self):
		for i, player in enumerate(self.game._players):
			if not player.userSession.isActive():
				del player

	def state(self, state):
		return self.sub_state == state

	def close_state(self):
    		if self.counterDown.finished:
			self.game._state += 1
		return self.game.state(WAITING_FOR_PLAYER)
