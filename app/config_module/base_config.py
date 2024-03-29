from datetime import timedelta

SECRET_KEY = 'KEY_KEY'  # Ключ для flask.session

NEED_PLAYERS_COUNT = 1# Количество игроков

# Константы времени (в секундах)
COUNT_DOWN_BEFORE_PREPARING__TIME = timedelta(seconds=0)
PREPARING_FOR_GAME__TIME = timedelta(seconds=0)
BID__TIME = timedelta(seconds=1)
EMULATION_STEP__TIME = timedelta(seconds=2)
USERSESSION_LIFETIME = 5000  # Время жизни UserSession

# Состояния объекта Game (их коды)
NONE_STATE = 0  # Не указано
WAITING_FOR_PLAYER = 1  # Ожидание игроков
PREPARING_FOR_GAME = 2  # Подготовка к игре
AUCTION = 3  # Аукцион
EMULATION = 4  # Эмуляция
RESULTS = 5  # Результаты


# sub_states waiting for player in Game (codes)
WAITING_FOR_PLAYER__WAIT = 0
WAITING_FOR_PLAYER__COUNTER_DOWN = 1


# Папки
STATIC_FOLDER = 'static'  # Папка со статическими файлам
TEMPLATE_FOLDER = 'templates'


# Файлы
LOTS_FILE = 'game-param/lots.csv'
LOTS_FILE_IN_AUCTION = 'app/static/game-param/lots.csv'
WEATHERCAST_FILE = 'game-param/weather.csv'
WEATHERCAST_FILE_IN_EMULATION = 'app/static/game-param/weather.csv'


# Наименования типов аукционов
HOLLAND__AUCTION_TYPE = 'dutch'
ENGLAND__AUCTION_TYPE = 'english'


#Константы для EMULATION
EMULATION_STEPS_COUNT = 200
PRICE_SELL_KVT = 1
PRICE_BUY_KVT = 100