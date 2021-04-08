from app.game_module.counter_down import CounterDown

from app.config_module.base_config import NONE_STATE, WAITING_FOR_PLAYER, PREPARING_FOR_GAME, PREPARING_FOR_GAME__TIME

class Preparing_for_game:
    '''
    It's a class for state PREPARING_FOR_GAME
    '''

    def __init__(self, game):
        '''
        Init function of preparing_for_game class
        '''
        self.game = game
        self.counterDown = CounterDown(PREPARING_FOR_GAME__TIME)

    def start(self):
        '''
        Method for start current state,
        actually it need for activate counterDown inside this object
        '''
        if self.game.state(PREPARING_FOR_GAME):
            self.counterDown.start()

    def close_state(self):
        '''
        Method for close current state and set next state
        '''
        if self.counterDown.finished and self.game.state(PREPARING_FOR_GAME):
            self.game.next_state()
        return not self.game.state(PREPARING_FOR_GAME)

    def getLotsDataAdress(self):
        '''
        Method for getting information about Lots in needed format
        '''
        return self.game.lots_file

    def getWetaherPredictionData(self, game):
        '''
        Method for getting information about weather prediction in needed format
        '''
        return self.game.weathercast_file
