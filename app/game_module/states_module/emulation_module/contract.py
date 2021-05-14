
class Contract:
    '''
    Класс для Контрактов, используемых для эмуляции
    '''

    def __init__(self, lot):
        '''
        Инициализация contract'a
        '''
        assert lot.is_purchased, 'illegal Contract'
        self.id = lot.id
        self.name = lot.name
        self.contract_type = lot.lot_type
        self.cost = lot.purchase_cost
        self.player = lot.who_bought

    def get_delta_result(self, weather_value):
        '''
        Method for get delta result of this contract
        '''
        if not (self.name in weather_value):
            return 0

        if self.contract_type == 'consumer':
            k = 1
        else:
            k = -1
        need_kvt = float(weather_value[self.name])
        return need_kvt, need_kvt * self.cost * k