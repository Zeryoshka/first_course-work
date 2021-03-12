from app.users_module.user import User


class Users():
    def __init__(self):
        self._users = []
        self._idForNewUser = 0

    def addUser(self):
        self._users.append(User(self._idForNewUser))
        self._idForNewUser += 1

        return self._users[-1].id

    def existUserWithId(self, user_id):
        for user in self._users:
            if user.id == user_id:
                return True
        return False

    def getUserById(self, user_id):
        for user in self._users:
            if user.id == user_id:
                return user
        assert(False)
