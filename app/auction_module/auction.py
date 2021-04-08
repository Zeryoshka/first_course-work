from app.auction_module.lot import Lot
import json
import csv


class Auction:
    def __init__(self):
        self.actual_lots = []
        self.sold_lots = []

    def parsing(self):
        csv_name = 'app/auction_module/test.csv'
        with open(csv_name) as csv_file:
            tmp = csv.reader(csv_file)

            for row in tmp:
                self.actual_lots.append(Lot(*row))

            self.actual_lots.pop(0)

            for lot in self.actual_lots:
                print(lot.return_info())

        for lot in self.actual_lots:
            if lot.lot_type == 'producer':
                lot.min_cost = 1
                lot.max_cost = 100
            elif lot.lot_type == 'consumer':
                lot.min_cost = 1
                lot.max_cost = 10
            else:
                assert 'Кривые данные'

    def export_as_json(self):
        return json.dumps(self.actual_lots + self.sold_lots)

    def analysing_bets(self, json_str):  # в строке "id игрока": "ставка"
        self.actual_lots[0].who_can_bid = list(
            json_str.keys)  # тут вообще словарь, а еще не работает так, как нужно, исправить
        pass  # хитрый анализ с выбором достойного

    def end_auction(self):
        self.actual_lots[0].status = 'sold'
        self.sold_lots.append(self.actual_lots[0])
        del (self.actual_lots[0])

    def return_lots_list(self):
        x = []
        for lot in self.actual_lots:
            x.append(lot.return_info())

        for lot in self.sold_lots:
            x.append(lot.return_info())

        return x


