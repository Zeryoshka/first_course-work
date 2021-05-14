from app.config_module.base_config import AUCTION, LOTS_FILE_IN_AUCTION
from app.config_module.base_config import BID__TIME

from .lot import Lot
from app.game_module.counter_down import CounterDown
import csv


class Auction:
    def __init__(self, game):
        self._is_started = False
        self.game = game
        self.actual_lots = []
        self.parsing()
        self._cur_lot_num = -1
        self.bid_counter_down = CounterDown(BID__TIME)

    def start(self):
        if (not self._is_started) and self.game.state(AUCTION):
            self._is_started = True
            self._cur_lot_num = 0
            self.bid_counter_down.start()
            self.cur_lot.make_lot_current()
        return self._is_started

    def close_state(self):
        if self._is_started and self._cur_lot_num == len(self.actual_lots):
            self.game.next_state()

    @property
    def cur_lot(self):
        return self.actual_lots[self._cur_lot_num]

    def parsing(self):
        '''
        парсинг из csv в список и предварительная обработка лотов
        '''
        csv_name = LOTS_FILE_IN_AUCTION  # TODO: Убери в конфиги, не позорься!!!
        with open(csv_name, encoding='utf-8') as csv_file:
            tmp = csv.DictReader(csv_file)
            for row in tmp:
                self.actual_lots.append(Lot(self.game.players,**row))

    def export_data(self): 
        '''
        возвращает список со всей инфой о каждом актуальном лоте
        '''
        x = []
        for lot in self.actual_lots:
            x.append(lot.return_info())

        return x

    def check_change_lot(self):
        '''
        Проверка смены лота
        '''
        if self.bid_counter_down.finished:
            self.bid_counter_down.clear()
            buyers_list, price = self.cur_lot.get_wins_buyers()
            if len(buyers_list) == 0:
                self.cur_lot.is_current = False
                self.start_next_lot_at_auction()
                return
            if len(buyers_list) == 1:
                buyer = buyers_list[0]
                self.cur_lot.make_lot_sold(buyer, price)
                self.start_next_lot_at_auction()
                return
            print('____________НЕСКОЛЬКО ИГРОКОВ____') #TODO Дописать обработку для этого случая
            buyer = buyers_list[0]
            self.cur_lot.make_lot_sold(buyer, price)
            self.start_next_lot_at_auction()

    def start_next_lot_at_auction(self):
        '''
        Установка нового лота в качестве текущего на аукцион
        '''
        self._cur_lot_num += 1
        if self._cur_lot_num == len(self.actual_lots):
            self.close_state()
            return
        self.cur_lot.make_lot_current()
        self.bid_counter_down.start()

    def make_bid(self, user, lot_id, price):
        '''
        Сделать ставку на текущий лот
        '''
        player = self.game.players.get_player_by_user(user)
        if lot_id != self.cur_lot.id:
            return (False, 'incorrect lot_id')
        is_valid, message = self.cur_lot.valid(player, price)
        if not is_valid:
            return (False, message)
        self.cur_lot.add_bid(player, price)
        return (True, 'bid is correctly')
