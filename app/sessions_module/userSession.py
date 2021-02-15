from os import urandom
from datetime import datetime, timedelta

_maxTimeWithoutActive = 100000

def _createToken():
    return urandom(20).hex()

class UserSession():
    def __init__(self, user):
        self.user = user
        self.token = _createToken()
        self._lastActiveTime = datetime.now()
    
    def updateActiveTime(self):
        self._lastActiveTime = datetime.now()
    
    def isActive(self):
        return datetime.now() - self._lastActiveTime <= timedelta(_maxTimeWithoutActive)
