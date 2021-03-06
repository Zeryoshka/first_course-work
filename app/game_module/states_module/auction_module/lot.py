from app.config_module.base_config import HOLLAND__AUCTION_TYPE, ENGLAND__AUCTION_TYPE
class Lot:
    def __init__(self, players, lot_id, lot_name, lot_type, auction_type, min_cost, max_cost):
        assert lot_type in ['producer', 'consumer'], 'Parse error'
        self.id = int(lot_id)
        self.name = lot_name
        self.lot_type = lot_type
        self.auction_type = auction_type
        self.is_current = False
        self.is_purchased = False
        self.who_bought = None
        self.purchase_cost = None
        self.min_cost = int(min_cost)
        self.min_start_cost = int(min_cost)
        self.max_cost = int(max_cost)
        self.max_start_cost = int(max_cost)
        self.who_can_make_bid = players
        self.bids = dict()
        self.auction_round = 1

    def make_lot_current(self):  # trivia
        self.is_current = True

    def valid(self, player, price):
        '''
        Проверка коректности ставки
        '''
        if not (player in self.who_can_make_bid):
            return False, 'incorrect player'
        if (self.min_cost > price) or (price > self.max_cost):
            return False, 'incorrect price'
        return True, 'correct'
    
    def user_have_bid(self, user):
        '''
        Проверка наличия ставки этим пользоватлем
        '''
        for id_ in self.bids:
            if user.id == id_:
                return True
        return False

    def get_user_bid(self, user):
        '''
        Получение ставки от конкретного пользователя
        '''
        return self.bids[user.id]

    def add_bid(self, player, price):
        '''
        Формирование ставки на lot
        '''
        self.bids[player.user.id] = price

    def get_wins_buyers(self):
        '''
        Анализ победителей борьбы за лот и победной цены
        '''
        if len(self.bids.values()) == 0:
            return [], None
        if self.auction_type == HOLLAND__AUCTION_TYPE:
            price = min(self.bids.values())
            self.max_cost = price
        elif self.auction_type == ENGLAND__AUCTION_TYPE:
            price = max(self.bids.values())
            self.min_cost = price
        else:
            assert False, "Неопознанный тип аукциона"

        # ids - cписок id player'ов, которые могут продолжать торговать
        ids = dict(filter(lambda x: x[1] == price, self.bids.items())).keys()
        buyers = list(map(self.who_can_make_bid.get_player_by_user_id, ids))
        return buyers, price

    def make_lot_sold(self, player, price):
        '''
        Анализ победителя лота
        '''
        self.is_purchased = True
        self.who_bought = player
        self.purchase_cost = price
        self.is_current = False

    def return_info(self):
        data = {
            'lot_id': self.id,
            'lot_name': self.name,
            'lot_type': self.lot_type,
            'is_current': self.is_current,
            'is_purchased': self.is_purchased,
            'min_cost': self.min_cost,
            'min_start_cost': self.min_start_cost,
            'max_cost': self.max_cost,
            'max_start_cost': self.max_start_cost,
            'auction_type': self.auction_type,
            'who_can_bid': list(map(lambda x: x.user.id, self.who_can_make_bid))
        }
        if data['is_purchased']:
            data['who_bought_id'] = self.who_bought.user.id
            data['who_bought_name'] = self.who_bought.user.name
            data['purchase_cost'] = self.purchase_cost
        return data
