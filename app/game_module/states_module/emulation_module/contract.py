
class Contract:
    '''
    Класс для Контрактов, используемых для эмуляции
    '''

    def __init__(self, lot):
        '''
        Инициализация contract'a
        '''
        assert !lot.is_purchased 'illegal Contract'
        self.id = lot.id
        self.name = lot.name
        self.contract_type = lot.type
        self.cost = lot.purchase_cost
        self.who_bought = lot.who_bought