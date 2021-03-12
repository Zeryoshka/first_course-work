from app.game_module.counter_down import CounterDown

from app.config_module.base_config import WAITING_FOR_PLAYER
from app.config_module.base_config import WAITING_FOR_PLAYER__COUNTER_DOWN, WAITING_FOR_PLAYER__WAIT
from app.config_module.base_config import COUNT_DOWN_BEFORE_PREPARING__TIME


class Waiting_for_player:
    '''
    It's a class for state WAITING_FOR_PLAYER
    '''
    def __init__(self, game):
        self.game = game
        self._sub_state = WAITING_FOR_PLAYER__WAIT
        self.counterDown = CounterDown(COUNT_DOWN_BEFORE_PREPARING__TIME)

    def addPlayer(self, userSession):
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
        if name not in ('game'):
            assert(self.game.players_count <= self.game.needPlayersCount)
        return object.__getattribute__(self, name)

    def delPlayersWithDiedSession(self):
        for i, player in enumerate(self.game.players):
            if not player.userSession.isActive():
                del player

    def state(self, state):
        return self._sub_state == state

    def close_state(self):
        if self.counterDown.finished and self.game.state(WAITING_FOR_PLAYER):
            self.game.next_state()
            print('****************************************************************************************************************')

        return self.game.state(WAITING_FOR_PLAYER)
