from datetime import datetime
from datetime import timedelta

class CounterDown:
    '''
    Class for synchronizing the countdown in game
    '''
    def __init__(self, time_len):
        assert isinstance(time_len, timedelta)
        self._time_len = time_len
        self._started = False
        self._start_time = datetime.now()

    def start(self):
        '''
        start counterdown and record start_time
        '''
        if not self.started
            self._started = True
            self._start_time = datetime.now()
        return self.started

    @property
    def started(self):
        return self._started

    @property
    def finished(self):
        return self.started and datetime.now() - self._start_time > self._time_len

    @property
    def left_time(self):
        return datetime.now() - self._start_time