import pathlib
import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime
import pickle

from Simulator import Simulator
from investors_types.HumanHeuristicsInvestors import *
from investors_types.PseudoAgents import *

from investors_types.RLInvestor import RLQInvestor, RLApproximateQInvestor

from RL_Trainer.QTable import QTable


# INITIAL_MONEY = 100000


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
    df.to_csv(results_file_name)
    end_time = time.time()
    print(f'\nFinished after {end_time - start_time} seconds.\nResults can be found in \'{results_file_name}\'')


def run_tests_by_investor(n, investor_type):
    if investor_type == RLQInvestor:
        rl_investor_args = {
            'q_table': QTable(pickle.load(open('Q-Table.pkl', "rb")))
        }
        run_tests(n, investor_type=investor_type, investor_kwargs=rl_investor_args)
    else:
        if investor_type == RLApproximateQInvestor:
            rl_investor_args = {
                'existing_weights': pathlib.Path.cwd() / 'approximate_q_learning_weights' / 'final_weights.pkl'
            }
            run_tests(n, investor_type=investor_type, investor_kwargs=rl_investor_args)
        else:
            run_tests(n, investor_type=investor_type)



if __name__ == '__main__':
    run_tests_by_investor(n=100, investor_type=RLQInvestor)


    # # Heuristic Agents
    # # run_tests(n=1000, investor_type=LowestFeeInvestor)
    #
    # # RL Agents
    # rl_investor_args = {
    #     'q_table': QTable(pickle.load(open('Q-Table.pkl', "rb")))
    # }
    # run_tests(n=25000, investor_type=RLQInvestor, investor_kwargs=rl_investor_args)
    #
    # # rl_investor_args = {
    # #     'existing_weights': pathlib.Path.cwd() / 'approximate_q_learning_weights' / 'final_weights.pkl'
    # # }
    # # run_tests(n=1000, investor_type=RLApproximateQInvestor, investor_kwargs=rl_investor_args)
