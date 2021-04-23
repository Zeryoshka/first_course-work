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

        

# TODO А как понять, кто купил?
# TODO Как потом это в эмуляцию добавить? (Это пока не горит)
    def make_lot_sold(self):  # trivia
        self.is_current = False
        self.is_purchased = True

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
