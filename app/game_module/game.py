from .states_module.waiting_for_player import Waiting_for_player
from .states_module.preparing_for_game import Preparing_for_game
from .states_module.auction_module.auction import Auction
from .players import Players
from app.config_module.base_config import NONE_STATE, WAITING_FOR_PLAYER, PREPARING_FOR_GAME, \
    AUCTION, EMULATION, RESULTS, COUNT_DOWN_BEFORE_PREPARING
from app.config_module.base_config import LOTS_FILE, WEATHERCAST_FILE
from app.config_module.base_config import NEED_PLAYERS_COUNT

class Game():
    '''
    Class for game object
    '''

    def __init__(self):
        '''
        Init function of Game class
        '''
        self._state = WAITING_FOR_PLAYER
        self._needPlayersCount = NEED_PLAYERS_COUNT
        self.players = Players()
        self.waiting_for_player = Waiting_for_player(self)
        self.preparing_for_game = Preparing_for_game(self)
        self.auction = Auction(self)
        self._lots_file = LOTS_FILE
        self._weathercast_file = WEATHERCAST_FILE

    @property
    def lots_file(self):
        '''
        Property for get file adress with information about lots
        '''
        return self._lots_file

    @property
    def weathercast_file(self):
        '''
        Property for getting file adress with weathercast
        '''
        return self._weathercast_file

    def state(self, state):
        '''
        Method for check state of game
        '''
        return self._state == state

    def next_state(self):
        '''
        Method for set next state of game
        !!!Don't use not in states objects from state_module!!!
        '''
        self._state += 1

    def userAddedToGame(self, userSession):
        '''
        Method for checking user with userSession with added to game
        '''
        return self.players.is_user_in_players(userSession)


    @property
    def needPlayersCount(self):
        '''
        Property for get needed players count
        '''
        return self._needPlayersCount
