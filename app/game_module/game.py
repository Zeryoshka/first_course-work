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
		self._state = WATITNG_FOR_PLAYER
		self.needPlayersCount = 2
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
	
	def userNotAddToGame(self, userSession):
		for player in self._players:
			if player.userSession == userSession:
				return False
		return True
	
	def delPlayersWithDiedSession(self):
		for i, player in enumerate(self._players):
			if not player.userSession.isActive():
				del self._players[i]

	def state_to_preparing_for_game(self):
		if self.is_waiting_for_player() and self.needPlayersCount == len(self._players):
			self._state = PREPARING_FOR_GAME
			return True
		return False

