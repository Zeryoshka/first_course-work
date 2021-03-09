from app.game_module.player import Player

from app.config_module.base_config import NONE_STATE, WAITING_FOR_PLAYER, PREPARING_FOR_GAME, \
	AUCTION, EMULATION, RESULTS, COUNT_DOWN_BEFORE_PREPARING

from app.config_module.base_config import COUNT_DOWN_BEFORE_PREPARING__TIME

from datetime import datetime, timedelta

class Game():
	
	def __init__(self):
		self._state = WAITING_FOR_PLAYER
		self.needPlayersCount = 3
		self._players = []
		self._time_start_count_down_before_preparing = datetime.now()
	
	def is_none_state(self):
		return self._state == NONE_STATE
	
	def is_waiting_for_player(self):
		return self._state == WAITING_FOR_PLAYER
	
	def is_preparing_for_game(self):
		return self._state == PREPARING_FOR_GAME
	
	def is_auction(self):
		return self._state == AUCTION

	def is_emulation(self):
		return self._state == EMULATION
	
	def is_resaults(self):
		return self._state == RESULTS

	def state(self, state):
		return self._state == state

	def addPlayer(self, userSession):
		self.delPlayersWithDiedSession()
		assert(self.is_waiting_for_player())
		assert(len(self._players) < self.needPlayersCount)
		self._players.append(Player(userSession))
	
	def userAddedToGame(self, userSession):
		for player in self._players:
			if player.userSession == userSession:
				return True
		return False
	
	def delPlayersWithDiedSession(self):
		for i, player in enumerate(self._players):
			if not player.userSession.isActive():
				del self._players[i]

	def state_to_count_down_before_preparing(self):
		print(f'{self._state} {len(self._players)}')
		if self.state(WAITING_FOR_PLAYER) and self.needPlayersCount == len(self._players):
			self._state = COUNT_DOWN_BEFORE_PREPARING
			self._time_start_count_down_before_preparing = datetime.now()
			return True
		return False
	
	def state_to_preparing_for_game(self):
		if self.state(COUNT_DOWN_BEFORE_PREPARING) and \
			self.count_down_1_active_time >= COUNT_DOWN_BEFORE_PREPARING__TIME:
			self._state = PREPARING_FOR_GAME
			return True
		else:
			return False

	@property
	def count_down_1_active_time(self):
		return datetime.now() - self.time_start_count_down_before_preparing
	
	@property
	def time_start_count_down_before_preparing(self):
		return self._time_start_count_down_before_preparing

	def get_players_count(self):
		return len(self._players)
