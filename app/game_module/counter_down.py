from datetime import datetime
from datetime import deltatime

class CounterDown:
    '''
    Class for synchronizing the countdown in game
    '''
    def __init__(self, time_len):
        self.time_len = time_len

    def start(self):
        self._time_start = datetime.now()

    def left_time(self):
        return datetime.now() - self._time_start

    def is_end(self):
        return datetime.now() - self._time_start > self.time_len