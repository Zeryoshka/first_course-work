import csv

from .emulation_timer import Emulation_timer
from .contract_utils import create_contracts
from .contract_utils import sort_contarcts_for_players

from app.config_module.base_config import EMULATION
from app.config_module.base_config import EMULATION_STEPS_COUNT
from app.config_module.base_config import EMULATION_STEP__TIME
from app.config_module.base_config import WEATHERCAST_FILE_IN_EMULATION
from app.config_module.base_config import PRICE_SELL_KVT
from app.config_module.base_config import PRICE_BUY_KVT

class Emulation:
    '''
    It's a class for state EMULATION
    '''

    def __init__(self, game):
        '''
        Init function of Emulation class
        '''
        self.game = game
        self.cur_step = 0
        self.step_time = EMULATION_STEP__TIME
        self.steps_count = EMULATION_STEPS_COUNT
        self.is_started = False
        self.contracts = dict()
        self.results_by_step = dict()
        self.weather_value = _read_of_weather_value()
        self.steps_timer = Emulation_timer(self.step_time, self.steps_count)

    def start(self):
        '''
        Method for start current state,
        '''
        if not self.game.state(EMULATION):
            return
        if self.is_started:
            return
            
        self.is_started = True
        self.cur_step = 0
        
        # Генерация основы results_by_step
        players_ids = list(map(lambda x: x.user.id, self.game.players))
        self.results_by_step = dict.fromkeys(players_ids, [0])

        self.contracts = sort_contarcts_for_players(
            create_contracts(self.game.auction.actual_lots),
            self.game.players
        )

        self.steps_timer.start()


    def close_state(self):
        '''
        Method for close current state and set next state
        '''
        if (self.cur_step > EMULATION_STEPS_COUNT) and \
         self.game.state(EMULATION):
            self.game.next_state()
        return not self.game.state(EMULATION)

    def check_and_change_step(self):
        '''
        Method for check and change step in Emulation object
        '''
        real_cur_step = self.steps_timer.real_step
        while real_cur_step > self.cur_step:
            self.cur_step += 1
            self.make_step()

    def make_step(self):
        '''
        Method for making of step
        '''
        print('it makes step')
        for player in self.game.players:
            player_contracts = self.contracts[player.user.id]
            value_for_cur_step = self.weather_value[self.cur_step - 1]
            
            kvt, new_result = 0, 0
            for contract in player_contracts:
                need_kvt, money = contract.get_delta_result(value_for_cur_step)
                new_result += money
                kvt += need_kvt
            if kvt > 0:
                new_result += kvt * PRICE_SELL_KVT
            else:
                new_result += kvt * PRICE_BUY_KVT

            last_res = self.results_by_step[player.user.id][-1]
            self.results_by_step[player.user.id].append(new_result + last_res)


    @property
    def cur_result(self):
        '''
        Current result of emulation in game
        '''
        ans = dict()
        for key, value in self.results_by_step.items():
            ans[key] = value[-1]
        return ans

def _read_of_weather_value():
    csv_name = WEATHERCAST_FILE_IN_EMULATION
    with open(csv_name, encoding='utf-8') as csv_file:
        tmp = csv.DictReader(csv_file)
        values = []
        for row in tmp:
            values.append(row)
    return values