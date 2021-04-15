from app.sessions_module.userSessions import UserSessions


class Lot:
    def __init__(self, id, name, lot_type, auction_type, min_cost, max_cost):
        self.id = id
        self.name = name
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
        self.who_can_bid = UserSessions.exportSessions()  # не придумал, как проверить. Если приходит список, все ок

    def is_purchased(self):  # продан ли лот
        if self.is_purchased:
            return True
        else:
            return False

    def is_current(self):  # текущий ли лот
        if self.is_current:
            return True
        else:
            return False

    def make_lot_current(self):  # trivia
        self.is_current = True

    def make_lot_sold(self):  # trivia
        self.is_current = False
        self.is_purchased = False

    def return_info(self):
        return {'lot_id': self.id, 'lot_name': self.name, 'lot_type': self.lot_type,
                'is_current': self.is_current, 'is_purchased': self.is_purchased, 'who_bought': self.who_bought,
                'purchase_cost': self.purchase_cost, 'min_cost': self.min_cost, 'min_start_cost': self.min_start_cost,
                'max_cost': self.max_cost, 'max_start_cost': self.max_start_cost, 'auction_type': self.auction_type,
                'who_can_bid': self.who_can_bid}


if __name__ == "__main__":
    lot1 = Lot(1223, 'user', [1, 3, 3], 100, 10000, 'english')
    print(lot1.return_info())
