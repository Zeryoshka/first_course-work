from app.game_module.player import Player

NONE_STATE = 0
WATITNG_FOR_PLAYER = 1
PREPARING_FOR_GAME = 2
AUCTION = 3
EMULATION = 4
RESAULTS = 5

"""
states:
	0 - none_state
	1 - waiting for player
	2 - preparing for game
	3 - auction
	4 - emulation 
	5 - resaults
"""
class Game():
	
	def __init__(self):
		self._state = NONE_STATE
		self.needPlayersCount = 4
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

	def addPlayer(self, user, userSession):
		assert(self.is_waiting_for_player())
		assert(self.needPlayersCount < len(self._players))
		self._players.append(Player(user, userSession))
	
	def state_to_preparing_for_game(self):
		if self.is_waiting_for_player() and self.needPlayersCount == len(self._players):
			self._state = PREPARING_FOR_GAME
			return True
		return False

