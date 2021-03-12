from app.game_module.counter_down import counterDown


class Preparing_for_game:
    '''
    It's a class for state PREPARING_FOR_GAME
    '''

    def __init__(self, game):
        '''
        Init function of preparing_for_game
        '''
        self.game = game
        self.counterDown = CounterDown(PREPARING_FOR_GAME__TIME)

    def start(self):
        if self.game.state(PREPARING_FOR_GAME):
            self.counterDown.start()

    def close_state(self):
        if self.counterDown.finished and self.game.state(PREPARING_FOR_GAME):
            self.game.next_state()
            print('****************************************************************************************************************')
        return self.game.state(WAITING_FOR_PLAYER)

    def getLotsDataAdress(self):
        '''
        Method for getting information about Lots in needed format
        '''
        return self.game.lots_file

    def getWetaherPredictionData(self, game):
        '''
        Method for getting information about weather prediction in needed format
        '''
        return self.game.weather_prediction_file
