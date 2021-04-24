from config_module.base_config import HOLLAND__AUCTION_TYPE, ENGLAND__AUCTION_TYPE

class Lot:
    def __init__(self, players, lot_id, lot_name, lot_type, auction_type, min_cost, max_cost):
        assert lot_type in ['producer', 'consumer'], 'Parse error'
        self.id = lot_id
        self.name = lot_name
        self.lot_type = lot_type
        self.auction_type = auction_type
        self.is_current = False
        self.is_purchased = False
        self.who_bought = None
        self.purchase_cost = None
        self.min_cost = min_cost
        self.min_start_cost = min_cost
        self.max_cost = max_cost
        self.max_start_cost = max_cost
        self.who_can_bet = players # не придумал, как проверить. Если приходит список, все ок
        self.bets = dict()
        self.auction_round = 1

    def make_lot_current(self):  # trivia
        self.is_current = True

    def valid(self, player, price):
        '''
        Проверка коректности ставки
        '''
        if not (player in self.who_can_bet):
            return False
        if not (self.min_cost < price < self.max_cost):
            return False
        return True

    def add_bet(self, player, price):
        '''
        Формирование ставки на lot
        '''
        self.bets[player.user.id] = price

    def get_wins_buyers(self):
        '''
        Анализ победителей борьбы за лот и победной цены
        '''
        if self.auction_type == HOLLAND__AUCTION_TYPE:
            price = min(self.bets.values())
            self.max_cost = price
        elif self.auction_type == ENGLAND__AUCTION_TYPE:
            price = max(self.bets.values())
            self.min_cost = price
        else:
            assert False, "Неопознанный тип аукциона"

        # ids - cписок id player'ов, которые могут продолжать торговать
        ids = dict(filter(lambda x: x[1] == price, self.bets.items())).keys()
        return ids, price

    def make_lot_sold(self, user, price):
        '''
        Анализ победителя лота
        '''
        self.who_bought = user
        self.is_current = False
        self.is_purchased = True
        self.purchase_cost = price

    def return_info(self):
        return {
            'lot_id': self.id,
            'lot_name': self.name,
            'lot_type': self.lot_type,
            'is_current': self.is_current,
            'is_purchased': self.is_purchased,
            'who_bought': self.who_bought,
            'purchase_cost': self.purchase_cost,
            'min_cost': self.min_cost,
            'min_start_cost': self.min_start_cost,
            'max_cost': self.max_cost,
            'max_start_cost': self.max_start_cost,
            'auction_type': self.auction_type,
            'who_can_bid': self.who_can_bet
        }
