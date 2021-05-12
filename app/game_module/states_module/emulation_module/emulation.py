from app.game_module.counter_down import CounterDown

from app.config_module.base_config import EMULATION
from app.config_module.base_config import EMULATION_STEPS_COUNT

class Emulation:
    '''
    It's a class for state EMULATION
    '''

    def __init__(self, game):
        '''
        Init function of Emulation class
        '''
        self.game = game
        self.cur_step = 0
        self.is_started = False
        # self.counterDown = CounterDown()

    def start(self):
        '''
        Method for start current state,
        actually it need for activate counterDown inside this object
        '''
        if not self.is_started and \
         self.game.state(EMULATION):
            self.is_started = True
            self.cur_step = 0
            # self.counterDown.start()

    def close_state(self):
        '''
        Method for close current state and set next state
        '''
        if (self.cur_step > EMULATION_STEPS_COUNT) and \
         self.game.state(EMULATION):
            self.game.next_state()
        return not self.game.state(EMULATION)
