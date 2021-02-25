SECRET_KEY = 'KEY_KEY' # Ключ для flask.session

USERSESSION_LIFETIME = 5000 # Время жизни UserSession

# Состояния объекта Game (их коды)
NONE_STATE = 0 # Не указано
WATITNG_FOR_PLAYER = 1 # Ожидание игроков
PREPARING_FOR_GAME = 2 # Подготовка к игре
AUCTION = 3 # Аукцион
EMULATION = 4 # Эмуляция
RESAULTS = 5 # Результаты

#Папки
STATIC_FOLDER = 'static' # Папка со статическими файлам
TEMPLATE_FOLDER = 'templates'