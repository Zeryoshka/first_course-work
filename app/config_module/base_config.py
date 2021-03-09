from datetime import timedelta

SECRET_KEY = 'KEY_KEY' # Ключ для flask.session

# Константы времени (в секундах)
COUNT_DOWN_BEFORE_PREPARING__TIME = timedelta(seconds=10) 
USERSESSION_LIFETIME = 5000 # Время жизни UserSession

# Состояния объекта Game (их коды)
NONE_STATE = 0 # Не указано
WATITNG_FOR_PLAYER = 1 # Ожидание игроков
COUNT_DOWN_BEFORE_PREPARING = 6 # Ожидание начала отсчета
PREPARING_FOR_GAME = 2 # Подготовка к игре
AUCTION = 3 # Аукцион
EMULATION = 4 # Эмуляция
RESAULTS = 5 # Результаты

#Папки
STATIC_FOLDER = 'static' # Папка со статическими файлам
TEMPLATE_FOLDER = 'templates'