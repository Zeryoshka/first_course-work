from app.auction_module.lot import Lot
import json
import csv


class Auction:
    def __init__(self):
        self.actual_lots = []
        self.sold_lots = []

    def parsing(self):  # парсинг из цсв в список и предварительная обработка лотов
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

    def export_as_json(self):  # возвращает json со всей инфой о каждом лоте
        x = []
        for lot in self.actual_lots:
            x.append(lot.return_info())

        for lot in self.sold_lots:
            x.append(lot.return_info())

        return json.dumps(x)

    def analysing_bets(self, bids):  # в приходящем словаре "id игрока": "ставка"
        self.actual_lots[0].who_can_bid = list(bids.keys)
        pass  # хитрый анализ с выбором достойного. Мне страшно за него браться

    def end_auction(self):  # метод завершения розыгрыша лота
        self.actual_lots[0].make_lot_sold()
        self.sold_lots.append(self.actual_lots[0])
        del (self.actual_lots[0])




