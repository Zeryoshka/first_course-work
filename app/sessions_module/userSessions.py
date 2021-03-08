from app.sessions_module.userSession import UserSession


class UserSessions():
    def __init__(self):
        self._sessions = []

    def addUserSesion(self, user):
        self._sessions.append(UserSession(user))
        return self._sessions[-1].token

    def existSessionWithToken(self, token):
        for session in self._sessions:
            if session.isActive():
                if session.token == token:
                    return True
            else:
                del session

        return False

    def getSessionByToken(self, token):
        for session in self._sessions:
            if session.token == token:
                return session
        assert (False)