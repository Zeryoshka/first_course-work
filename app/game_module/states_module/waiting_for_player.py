from app.game_module.counter_down import CounterDown

from app.config_module.base_config import WAITING_FOR_PLAYER
from app.config_module.base_config import WAITING_FOR_PLAYER__COUNTER_DOWN, WAITING_FOR_PLAYER__WAIT
from app.config_module.base_config import COUNT_DOWN_BEFORE_PREPARING__TIME


class Waiting_for_player:
    '''
    It's a class for state WAITING_FOR_PLAYER
    '''

    def __init__(self, game):
        '''
        Init Method for class Waiting for player
        '''
        self.game = game
        self._sub_state = WAITING_FOR_PLAYER__WAIT
        self.counterDown = CounterDown(COUNT_DOWN_BEFORE_PREPARING__TIME)

    def addPlayer(self, userSession):
        '''
        Method for add user to game
        '''
        self.game.players.append(Player(userSession))

    def needMorePlayer(self):
        return (self.game.players_count < self.game.needPlayersCount)

    def start_timer(self):
        self.delPlayersWithDiedSession()
        if (self.game.players_count == self.game.needPlayersCount):
            self.counterDown.start()
            self._sub_state = WAITING_FOR_PLAYER__COUNTER_DOWN
        return self.counterDown.started

    def __getattribute__(self, name):
        '''
        It needs for check and make assert in case of error
        when game.players_count > self.game.needPlayersCount
        '''
        if name not in ('game'):
            assert(self.game.players_count <= self.game.needPlayersCount)
        return object.__getattribute__(self, name)

    def delPlayersWithDiedSession(self):
        '''
        Method for delete user with_died session form players
        '''
        for i, player in enumerate(self.game.players):
            if not player.userSession.isActive():
                del player

    def state(self, state):
        '''
        Method for check sub_state of class state
        '''
        return self._sub_state == state

    def close_state(self):
        '''
        It needs for close state in case end of state
        '''
        if self.counterDown.finished and self.game.state(WAITING_FOR_PLAYER):
            self.game.next_state()

        return self.game.state(WAITING_FOR_PLAYER)
