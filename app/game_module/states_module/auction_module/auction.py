from lot import Lot
import json
import csv

# TODO аукцион это state для game поэтому он должен лежать в соответствующем пакете
# Метод start для ацкциона, чтобы начинать 
# Иметь метод close_state для перехода game к следующему состоянию
# Иметь возможность розыгргыша лота, возможность начать его продавать
# А обратный отсчет где? (Там для этог есть класс)
# А как ставку сдлеать?
# А где render_param, чтобы параметры для страничек делать?
class Auction:
    def __init__(self):
        self.actual_lots = []
        self.sold_lots = []

    def parsing(self):  # парсинг из цсв в список и предварительная обработка лотов
        csv_name = 'app/auction_module/test.csv' # TODO: Убери в конфиги, не позорься!!!
        with open(csv_name, encoding='utf-8') as csv_file:  ## Да не позорюсь я, это заготовка!!!
            tmp = csv.DictReader(csv_file)
            for row in tmp:
                self.actual_lots.append(Lot(**row))

            for lot in self.actual_lots:
                print(lot.return_info())

        #TODO Почему проверка идет после того, как лоты были созданы? Логичнее всего это встроить в сам Lot
        #Зачем ты переобъявляешь параметры? Зачем тогда вообще lot нужен?
        for lot in self.actual_lots:
            if lot.lot_type == 'producer':
                lot.min_cost = 1 # Вот это вот зачем?
                lot.max_cost = 100 # Вот это вот зачем?
            elif lot.lot_type == 'consumer':
                lot.min_cost = 1 # Вот это вот зачем?
                lot.max_cost = 10 # Вот это вот зачем?
            else:
                assert False, 'Кривые данные'
                # Топ вариант для проверки:
                # assert lot_type in ['producer', 'consumer'], 'Parse error'
                # (Понятно, что массивчик достается из конфигов)
                # А еще надо проверить тип аукциона, это же тоже строка!!
                # Еще все параметры, кроме разве что name
                # И преобразовать cost и всякое такое к числам
                # Можешь отдельный модуль конфигов пределать к текущему пакету конфигов, чтобы был чисто для аукциона

    def export_data(self):  # возвращает json со всей инфой о каждом лоте
        x = []
        for lot in self.actual_lots:
            x.append(lot.return_info())

        for lot in self.sold_lots:
            x.append(lot.return_info())

        return x

    def analysing_bets(self, bids):  # в приходящем словаре "id игрока": "ставка"
        self.actual_lots[0].who_can_bid = list(bids.keys) # Почему 0!?!?!?!?!?!?
        # хитрый анализ с выбором достойного. Мне страшно за него браться

    def end_auction(self):  # метод завершения розыгрыша лота
        self.actual_lots[0].make_lot_sold()# Почему 0!?!?!?!?!?!?
        self.sold_lots.append(self.actual_lots[0])# Почему 0!?!?!?!?!?!?
        del (self.actual_lots[0])# Почему 0!?!?!?!?!?!?
