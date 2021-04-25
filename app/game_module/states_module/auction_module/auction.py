from app.config_module.base_config import AUCTION
from app.config_module.base_config import BET__TIME

from .lot import Lot
from app.game_module.counter_down import CounterDown
import csv

# Метод start для ацкциона, чтобы начинать
# Иметь метод close_state для перехода game к следующему состоянию
# Иметь возможность розыгргыша лота, возможность начать его продавать
# А обратный отсчет где? (Там для этог есть класс)
# А как ставку сдлеать?
# А где render_param, чтобы параметры для страничек делать?


class Auction:
    def __init__(self, game):
        self._is_started = False
        self.game = game
        self.actual_lots = []
        self.parsing()
        self._cur_lot_num = -1
        self.bet_counter_down = CounterDown(BET__TIME)

    def start(self):
        if (not self._is_started) and self.game.state(AUCTION):
            self._is_started = True
            self._cur_lot_num = 0
            self.bet_counter_down_lot_num = 0
            self.bet_counter_down.start()
        return self._is_started

    def close_state(self):
        if self._is_started and self._cur_lot_num == len(self.actual_lots):
            self.game.state += 1

    @property
    def cur_lot(self):
        return self.actual_lots[self._cur_lot_num]

    def parsing(self):
        '''
        парсинг из csv в список и предварительная обработка лотов
        '''
        csv_name = 'app/static/game-param/lots.csv'  # TODO: Убери в конфиги, не позорься!!!
        with open(csv_name, encoding='utf-8') as csv_file:
            tmp = csv.DictReader(csv_file)
            for row in tmp:
                self.actual_lots.append(Lot(self.game.players,**row))
                # А еще надо проверить тип аукциона, это же тоже строка!!
                # Еще все параметры, кроме разве что name
                # И преобразовать cost и всякое такое к числам
                # Можешь отдельный модуль конфигов пределать к текущему пакету конфигов, чтобы был чисто для аукциона

    def export_data(self): 
        '''
        возвращает список со всей инфой о каждом актуальном лоте
        '''
        x = []
        for lot in self.actual_lots:
            x.append(lot.return_info())

        return x

    # TODO Это правильнее будет запихать в сам лот,
    # метод будет возвращать список юзеров, которые могут дальше бодаться
    # Причем в make_lot_sold()

    def check_change_lot(self):
        '''
        Проверка смены лота
        '''
        if self.bet_counter_down.finished:
            self.bet_counter_down.clear()
            buyers_list, price = self.cur_lot.get_wins_buyers()
            if len(buyers_list) == 1:
                buyer = buyers_list[0]
                self.cur_lot.make_lot_sold(buyer, price)
                self.start_next_lot_at_auction()
            else:
                print('____________НЕСКОЛЬКО ИГРОКОВ____') #TODO Дописать обработку для этого случая

    def start_next_lot_at_auction(self):
        '''
        Установка нового лота в качестве текущего на аукцион
        '''
        self._cur_lot_num += 1
        if self._cur_lot_num == len(self.actual_lots):
            self.game.close_state()
            return
        self.bet_counter_down.start()

    def make_bet(self, user, lot_id, price):
        '''
        Сделать ставку на текущий лот
        '''
        player = self.game.get_player_by_user(user)
        if lot_id != self.cur_lot.id:
            return (False, 'incorrect lot_id')
        if not self.cur_lot.valid(player, price):
            return (False, 'incorrect price')
        self.cur_lot.add_bet(player, price)
        return (True, 'bet is correctly')
