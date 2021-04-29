import pathlib

import pandas as pd

from Printer import *
from gym_simulator.envs.custom_env import CustomEnv
from investors_types.HumanInvestor import HumanInvestor
from investors_types.HumanHeuristicsInvestors import *
from investors_types.PseudoAgents import *

from investors_types.RLInvestor import RLQInvestor, RLApproximateQInvestor
# from investors_types.RLInvestor import RLQInvestor
# from investors_types.RLInvestor import RLApproximateQInvestor

from gym_simulator.envs.QTable import QTable
import pickle


class Simulator:
    def __init__(self, funds_csv, funds_list_names, investor, investor_kwargs=None):
        self._env = CustomEnv(funds_csv, funds_list_names, investor, investor_kwargs)

    def run_simulator(self):
        funds_in_this_run = self._env.get_funds_symbols_in_this_run()
        funds_symbols_str = self._env.get_funds_in_this_run_str()
        funds_by_quarters, money_by_quarter = [], [self._env.get_investor_money()]

        done = False
        initial_state = self._env.reset()
        curr_state = initial_state
        while not done:
            action = self._env.investor_action(curr_state)
            next_state, reward, done, _ = self._env.step(action)
            curr_state = next_state
            # funds_by_quarters.append(action)
            funds_by_quarters.append(funds_in_this_run[action])
            money_by_quarter.append(self._env.get_investor_money())

        res = [funds_symbols_str] + funds_by_quarters + money_by_quarter
        return res

    def get_investor(self):
        return self._env.get_investor()


if __name__ == '__main__':
    rl_investor_args = {
        'q_table': QTable(pickle.load(open('Q-Table.pkl', "rb")))
    }
    funds_df = pd.read_csv('funds_after_processing.csv').set_index('fund_symbol')
    funds_names = funds_df.index.unique().tolist()

    sim = Simulator(funds_csv=funds_df, funds_list_names=funds_names, investor=RLQInvestor,
                    investor_kwargs=rl_investor_args)

    results_line = sim.run_simulator()
    # todo: add rl q learning trainer
    # todo: make sure approx q learning works correctly after refactoring
    Printer.print_results_path(results_line)
    Printer.print_final_results(sim.get_investor())

    # rl_investor_args = {
    #     'existing_weights': pathlib.Path.cwd() / 'approximate_q_learning_weights' / 'final_weights.pkl'
    # }
    # funds_df = pd.read_csv('funds_after_processing.csv').set_index('fund_symbol')
    # funds_names = funds_df.index.unique().tolist()
    #
    # sim = Simulator(funds_csv=funds_df, funds_list_names=funds_names, investor=RLApproximateQInvestor,
    #                 investor_kwargs=rl_investor_args)
    #
    # results_line = sim.run_simulator()
    # # todo: add rl q learning trainer
    # # todo: make sure approx q learning works correctly after refactoring
    # Printer.print_results_path(results_line)
    # Printer.print_final_results(sim.get_investor())