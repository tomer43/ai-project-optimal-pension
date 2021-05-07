import pathlib
import pickle

import pandas as pd

from our_simulator.Printer import *
from our_simulator.CustomEnv import CustomEnv
from investors_types.HumanHeuristicsInvestors import *
from investors_types.PseudoAgents import *
from investors_types.RLInvestor import RLQInvestor, RLApproximateQInvestor
from RL_Trainer.QTable import QTable


def run_simulator_by_investor(investor_type):
    """
    Entry point function to run a single simulator and print results. It handles input for different investors,
    currently relevant only for RL based investors. Then it calls to run_simulator.
    :param investor_type: (type) a class name, must be an investor type.
                            Notice this should be type and not an instance.
    """
    funds_df = pd.read_csv('funds_after_processing.csv').set_index('fund_symbol')
    funds_names = funds_df.index.unique().tolist()
    investor_args = {}
    if investor_type == RLQInvestor:
        # Expecting to get an existing trained agent - run this after running TrainerQLearning
        investor_args['q_table'] = QTable(pickle.load(open(r'./q_learning_q_table/Q-Table.pkl', "rb")))
    elif investor_type == RLApproximateQInvestor:
        # Expecting to get an existing trained agent - run this after running TrainerApproximateRL
        investor_args['existing_weights'] = pathlib.Path.cwd() / 'approximate_q_learning_weights' / 'final_weights.pkl'

    sim = Simulator(funds_csv=funds_df, funds_list_names=funds_names, investor=investor_type,
                    investor_kwargs=investor_args)

    results_line = sim.run_simulator()
    Printer.print_results_path(results_line)
    Printer.print_final_results(sim.get_investor())


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
            funds_by_quarters.append(funds_in_this_run[action])
            money_by_quarter.append(self._env.get_investor_money())

        res = [funds_symbols_str] + funds_by_quarters + money_by_quarter
        return res

    def get_investor(self):
        return self._env.get_investor()


if __name__ == '__main__':
    # To run simulator, simply call to run_simulator_by_investor function with an investor_type, see example below.
    # Results will be printed to screen.
    # In order to run a RL agent, you should first train separately using "TrainerRL.py" in "RL_Trainer" folder.
    # Running a pseudo-agent requires uncommenting a line in State.py
    run_simulator_by_investor(investor_type=LowestFeeInvestor)
