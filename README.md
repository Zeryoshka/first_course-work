# Power market
Power Market - стратегическая экономическая многопользовательская онлайн игра, эмулирующая работу распределенной энергетической сети. Данный проект являлся курсовой работой студента первого курса в МИЭМ НИУ ВШЭ.

## Суть игры
Каждый игрок представляет собой энергетическую компанию, которая может заключать контракты, на получение и предоставление электроэнергии, однако для залючения контракта надо выиграть на аукционе.  
Цель игрока заработать наибольшее количество денег

## Особенности реализации
Для запуска игры на нескольких устройствах необходимо развернуть сервер и подключиться к нему.
Серверная часть игры разработана на python с использованием фреймворка flask, также из библиотек, не включенных в стандартный пакет, использовалась random-username.  
На клиентской стороне использовался js совместно с jquery.
Текущая реализация игры предусматривает возможность серьезного расширения. Предусмотрена регистрация и аутентификация игроков, но в остутствии бд я храню все в опертивной памяти, поэтому после каждого запуска регистрациия производится повтороно (Но автоматически, после нажатия на кнопку).
Основные настройки можно изменить в файле base_config.py (Коментарии достаточно точно отражают содержимое переменных)

## Запуск
Для запуска необходимо запустить файл run-serve.py, а для запуска в отладочном редиме необходимо запустить файл run-debug.py 
