from our_simulator.SimulatorCore import SimulatorCore
from investors_types.Investor import Investor


INITIAL_MONEY = 100000
DEBUG_MODE = False


class CustomEnv:
    def __init__(self, funds_csv, funds_names, investor=Investor, investor_kwargs=None):
        if investor_kwargs is None:
            investor_kwargs = {}
        self._investor = investor(INITIAL_MONEY, **investor_kwargs)
        self._pygame = SimulatorCore(funds_csv, debug_mode=DEBUG_MODE, funds_names=funds_names, investor=self._investor)
        self._fund_csv = funds_csv
        self._funds_names = funds_names

    def reset(self):
        del self._pygame
        self._investor.reset_money()
        self._pygame = SimulatorCore(df=self._fund_csv, investor=self._investor, debug_mode=DEBUG_MODE,
                                     funds_names=self._funds_names)
        obs = self._pygame.observe()
        return obs

    def step(self, action):
        self._pygame.action(action)
        obs = self._pygame.observe()
        reward = self._pygame.evaluate()
        done = self._pygame.is_done()
        return obs, reward, done, {}

    def investor_action(self, state):
        return self._investor.choose_fund(state)

    def get_funds_symbols_in_this_run(self):
        return [fund.get_symbol() for fund in self._pygame.get_funds()]

    def get_funds_in_this_run_str(self):
        return self._pygame.get_funds_symbol()

    def get_investor_money(self):
        return self._investor.get_money()

    def get_investor(self):
        return self._investor
