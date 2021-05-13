
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
        if lot.who_bought is None:
            print(f'{lot.id} {lot.name} {lot.purchase_cost} {lot.is_purchased}')
        self.player = lot.who_bought