import gym
import pandas as pd
from investors_types.HumanHeuristicsInvestors import *
# from investors_types.RLInvestor import RLApproximateQInvestor
from gym_simulator.envs.SimulatorCore import SimulatorCore


NUM_OF_HUMAN_HEURISTICS = 6
INITIAL_MONEY = 100000
DEBUG_MODE = True


class CustomEnv(gym.Env):
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

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def seed(self, seed=None):
        pass

    def investor_action(self, state):
        return self._investor.choose_fund(state)

    # def get_funds_in_this_run(self):
    #     return self._pygame.get_funds_symbol()

    def get_funds_symbols_in_this_run(self):
        return [fund.get_symbol() for fund in self._pygame.get_funds()]

    def get_funds_in_this_run_str(self):
        return self._pygame.get_funds_symbol()

    def get_investor_money(self):
        return self._investor.get_money()

    # def get_investor_estimator(self):
    #     if isinstance(self._investor, RLApproximateQInvestor):
    #         return self._investor.get_inner_estimator()
    #     else:
    #         raise RuntimeError("Can't call to get_investor_estimator method for non RL investors")

    def get_investor(self):
        return self._investor
