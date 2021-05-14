from math import floor

from app.game_module.counter_down import CounterDown

class Emulation_timer(CounterDown):
    '''
    Class for timer of steps in Emulation state of Game
    '''

    def __init__(self, time_for_step, steps_count):
        '''
        Init funciton for Emulation_timer
        '''
        self.step_time_len = time_for_step
        self.steps_count = steps_count
        super().__init__(time_for_step * steps_count)

    @property
    def real_step(self):
        '''
        Number of real step of Emulation
        '''
        return floor(self.time_from_start / self.step_time_len)

    @property
    def left_time_befor_new_step(self):
        '''
        Left time befor new step will start
        '''
        return (self.real_step + 1) * self.step_time_len - self.time_from_start