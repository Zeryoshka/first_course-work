from datetime import datetime
from datetime import timedelta


class CounterDown:
    '''
    Class for synchronizing the countdown in game
    '''

    def __init__(self, time_len):
        assert isinstance(time_len, timedelta)
        self._remember_time_len = time_len
        self._time_len = time_len
        self._started = False

    def start(self):
        '''
        start counterdown and record start_time
        '''
        if not self.started:
            self._started = True
            self._start_time = datetime.now()
        return self.started

    @property
    def started(self):
        return self._started

    @property
    def finished(self):
        return self.started and self.left_time == timedelta(0)

    @property
    def left_time(self):
        if self.started and datetime.now() - self._start_time < self._time_len:
            return self._time_len - (datetime.now() - self._start_time)
        return timedelta(0)

    @property
    def time_from_start(self):
        if self.started:
            return timedelta(0)
        return datetime.now() - self._start_time
    
    def clear(self):
        self._time_len = self._remember_time_len
        self._started = False
