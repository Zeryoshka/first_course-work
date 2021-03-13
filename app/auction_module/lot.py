import json


class Lot:
    def __init__(self, lot_id, lot_name, lot_type, lot_params, min_cost, min_start_cost, max_cost, max_start_cost,
                 auction_type, who_can_bid):
        self.lot_id = lot_id
        self.status = 'not sold'
        self.lot_name = lot_name
        self.lot_type = lot_type
        self.lot_params = lot_params
        self.if_purchased = False
        self.who_bought = ''
        self.purchase_cost = 0
        self.min_cost = min_cost
        self.min_start_cost = min_start_cost
        self.max_cost = max_cost
        self.max_start_cost = max_start_cost
        self.auction_type = auction_type
        self.who_can_bid = who_can_bid

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
        return {'lot_id': self.lot_id, 'status': self.status, 'lot_name': self.lot_name, 'lot_type': self.lot_type,
                'lot_params': self.lot_params, 'if_purchased': self.if_purchased, 'who_bought': self.who_bought,
                'purchase_cost': self.purchase_cost, 'min_cost': self.min_cost, 'min_start_cost': self.min_start_cost,
                'max_cost': self.max_cost, 'max_start_cost': self.max_start_cost, 'auction_type': self.auction_type,
                'who_can_bid': self.who_can_bid}


if __name__ == "__main__":
    lot1 = Lot(1223, 'bepis', 'user', [1, 3, 3], 100, 1200, 10000,
               1000000, 'english', [1, 2, 3])
    print(lot1.return_info())
