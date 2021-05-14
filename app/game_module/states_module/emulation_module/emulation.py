from .emulation_timer import Emulation_timer
from .contract_utils import create_contracts
from .contract_utils import sort_contarcts_for_players

from app.config_module.base_config import EMULATION
from app.config_module.base_config import EMULATION_STEPS_COUNT
from app.config_module.base_config import EMULATION_STEP__TIME

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
        # for player in self.game.players:
        # new_result = self.contracts[player.user.id]
        # self.results_by_step[player.user.id].append(new_result)

    @property
    def cur_result(self):
        '''
        Current result of emulation in game
        '''
        ans = dict()
        for key, value in self.results_by_step.items():
            ans[key] = value[-1]
        return ans