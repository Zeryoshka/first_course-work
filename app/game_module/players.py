from .player import Player
class Players():
    '''
    Класс для всех игроков
    '''

    def __init__(self, lst = None):
        '''
        Инициализация объекта класса Players
        '''
        if lst is None:
            lst = []
        self._players = lst

    def __getitem__(self, key):
        '''
        Итерация для объекта Players
        '''
        if isinstance(key, int):
            return self._players[key]
        if isinstance(key, slice):
            return self.__class__(self._players[key.start:key.stop:key.step])
        raise ValueError()
            
    def add_player(self, user, user_session):
        '''
        Добавление player'а к players
        '''
        self._players.append(Player(user, user_session))

    def get_player_by_user(self, user):
        '''
        Поиск player'а по user's
        '''
        for player in self._players:
            if player.user == user:
                return player
        raise ValueError

    def get_player_by_user_id(self, id_):
        '''
        Поиск player по id
        '''
        for player in self._players:
            if player.user.id == id_:
                return player
        raise ValueError
    
    def is_user_in_players(self, user_session):
        '''
        Method for checking user with user_session with added to players
        '''
        for player in self._players:
            if player.userSession == user_session:
                return True
        return False

    @property
    def players_count(self):
        '''
        Property for getting current players count
        '''
        return len(self._players)
