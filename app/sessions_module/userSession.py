from os import urandom
from datetime import datetime, timedelta

from app.config_module.base_config import USERSESSION_LIFETIME

def _createToken():
    return urandom(20).hex()

class UserSession():
    def __init__(self, user):
        self.user = user
        self.token = _createToken()
        self._lastActiveTime = datetime.now()
        print(timedelta(USERSESSION_LIFETIME))

    
    def updateActiveTime(self):
        self._lastActiveTime = datetime.now()
    
    def isActive(self):
        return datetime.now() - self._lastActiveTime <= timedelta(seconds = USERSESSION_LIFETIME)
