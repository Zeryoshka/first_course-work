from app.game_module.player import Player

from app.config_module.base_config import NONE_STATE, WATITNG_FOR_PLAYER, PREPARING_FOR_GAME, \
	AUCTION, EMULATION, RESAULTS

class Game():
	
	def __init__(self):
		self._state = WATITNG_FOR_PLAYER
		self.needPlayersCount = 3
		self._players = []
	
	def is_none_state(self):
		return self._state == NONE_STATE
	
	def is_waiting_for_player(self):
		return self._state == WATITNG_FOR_PLAYER
	
	def is_preparing_for_game(self):
		return self._state == PREPARING_FOR_GAME
	
	def is_auction(self):
		return self._state == AUCTION

	def is_emulation(self):
		return self._state == EMULATION
	
	def is_resaults(self):
		return self._state == RESAULTS

	def addPlayer(self, userSession):
		self.delPlayersWithDiedSession()
		assert(self.is_waiting_for_player())
		assert(len(self._players) < self.needPlayersCount)
		self._players.append(Player(userSession))
		self.state_to_preparing_for_game()
	
	def userAddedToGame(self, userSession):
		for player in self._players:
			if player.userSession == userSession:
				return True
		return False
	
	def delPlayersWithDiedSession(self):
		for i, player in enumerate(self._players):
			if not player.userSession.isActive():
				del self._players[i]

	def state_to_preparing_for_game(self):
		if self.is_waiting_for_player() and self.needPlayersCount == len(self._players):
			self._state = PREPARING_FOR_GAME
			return True
		return False
	def get_players_count(self):
		return len(self._players)

