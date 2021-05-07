import pathlib
import time
from datetime import datetime
import pickle

import pandas as pd
from tqdm import tqdm

from Simulator import Simulator
from investors_types.HumanHeuristicsInvestors import *
from investors_types.PseudoAgents import *
from investors_types.RLInvestor import RLQInvestor, RLApproximateQInvestor
from RL_Trainer.QTable import QTable


def get_columns_names():
    return ['funds_this_run'] + [f'fund_q{i+1}' for i in range(43)] + [f'money_q{i}' for i in range(44)]


def get_results_file_name(investor_type):
    file_name = investor_type.__name__ + '_results '
    now = datetime.now()
    date_time = now.strftime("%d.%m.%Y %H-%M-%S")
    file_name += date_time + '.csv'
    return file_name


def run_tests(n, investor_type, investor_kwargs=None):
    print(f'Running {n} tests for {investor_type.__name__}...')
    start_time = time.time()
    df = pd.read_csv('funds_after_processing.csv').set_index('fund_symbol')
    results = []
    funds_names = df.index.unique().tolist()
    for _ in tqdm(range(n), desc="\tTesting Progress"):
        sim = Simulator(funds_csv=df, investor=investor_type, funds_list_names=funds_names,
                        investor_kwargs=investor_kwargs)
        result = sim.run_simulator()
        results.append(result)
    df = pd.DataFrame(results, columns=get_columns_names())
    results_file_name = get_results_file_name(investor_type)
    df.to_csv(pathlib.Path.cwd() / 'experiments_results' / results_file_name)
    end_time = time.time()
    print(f'\nFinished after {end_time - start_time} seconds.\nResults can be found in \'{results_file_name}\'')


def run_tests_by_investor(n, investor_type):
    """
    Entry point function to run various tests and export if to a csv. It handles input for different investors,
    currently relevant only for RL based investors. Then it calls to run_tests which perform the tests and save results.
    :param n:               (int) number of tests to run
    :param investor_type:   (type) a class name, must be an investor type.
                             Notice this should be type and not an instance.
    """
    investor_args = {}
    if investor_type == RLQInvestor:
        # Expecting to get an existing trained agent - run this after running TrainerQLearning
        investor_args['q_table'] = QTable(pickle.load(open('./q_learning_q_table/Q-Table.pkl', 'rb')))
    elif investor_type == RLApproximateQInvestor:
        # Expecting to get an existing trained agent - run this after running TrainerApproximateRL
        investor_args['existing_weights'] = pathlib.Path.cwd() / 'approximate_q_learning_weights' / 'final_weights.pkl'

    run_tests(n, investor_type=investor_type, investor_kwargs=investor_args)


if __name__ == '__main__':
    # To run tests, simply call to run_tests_by_investor function with an investor_type and n (number of tests).
    # See example below. Results will be saved as a csv file in experiments_results folder.
    # In order to run a RL agent, you should first train separately using "TrainerRL.py" in "RL_Trainer" folder.
    # Running a pseudo-agent requires uncommenting a line in State.py
    run_tests_by_investor(n=100, investor_type=RLQInvestor)
