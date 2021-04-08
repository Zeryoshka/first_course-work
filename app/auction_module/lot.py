from app.sessions_module.userSessions import UserSessions

class Lot:
    def __init__(self, id, name, lot_type, auction_type, min_cost, max_cost):
        self.id = id
        self.status = 'not sold'
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
        self.who_can_bid = UserSessions.exportSessions()

    def is_not_sold(self):
        if self.status == 'not sold':
            return True
        else:
            return False

    def is_current(self):
        if self.status == 'current':
            return True
        else:
            return False

    def is_sold(self):
        if self.status == 'sold':
            return True
        else:
            return False

    def make_lot_current(self):
        pass

    def return_info(self):
        return {'lot_id': self.id, 'status': self.status, 'lot_name': self.name, 'lot_type': self.lot_type,
                'is_current': self.is_current, 'is_purchased': self.is_purchased, 'who_bought': self.who_bought,
                'purchase_cost': self.purchase_cost, 'min_cost': self.min_cost, 'min_start_cost': self.min_start_cost,
                'max_cost': self.max_cost, 'max_start_cost': self.max_start_cost, 'auction_type': self.auction_type,
                'who_can_bid': self.who_can_bid}


if __name__ == "__main__":
    lot1 = Lot(1223, 'user', [1, 3, 3], 100, 10000, 'english')
    print(lot1.return_info())
