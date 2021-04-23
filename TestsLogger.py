import pandas as pd
from Simulator import Simulator
from investors_types.HumanHeuristicsInvestors import *
from investors_types.PseudoAgents import *
from investors_types.RLInvestor import RLInvestor
import time
from datetime import datetime
from gym_simulator.envs.TrainerRL import TrainerRL
from Config import *

from tqdm import tqdm

INITIAL_MONEY = 100000


def get_columns_names():
    return ['funds_this_run'] + [f'fund_q{i+1}' for i in range(43)] + [f'money_q{i}' for i in range(44)]


def get_results_file_name(investor_type):
    file_name = investor_type.__name__ + '_results '
    now = datetime.now()
    date_time = now.strftime("%d.%m.%Y %H-%M-%S")
    file_name += date_time + '.csv'
    return file_name


def run_tests(n, investor_type, debug_mode=False):
    print(f'Running {n} tests for {investor_type.__name__}...')
    start_time = time.time()
    df = pd.read_csv('funds_after_processing.csv')
    results = []
    funds_names = df['fund_symbol'].unique().tolist()
    if investor_type == RLInvestor:
        q_table = TrainerRL(max_episodes=NUM_OF_EPISODES).train()
    else:
        q_table = None
    for _ in tqdm(range(n), desc="\tTesting Progress"):
        sim = Simulator(df, INITIAL_MONEY, investor_type, debug_mode, funds_names, q_table)
        result = sim.run_simulator()
        results.append(result)
    df = pd.DataFrame(results, columns=get_columns_names())
    results_file_name = get_results_file_name(investor_type)
    df.to_csv(results_file_name)
    end_time = time.time()
    print(f'\nFinished after {end_time - start_time} seconds.\nResults can be found in \'{results_file_name}\'')


if __name__ == '__main__':
    run_tests(NUM_OF_EXPERIMENTTS, RLInvestor, debug_mode=DEBUG_MODE)

# -----------------------------------------------------------------------------
# import pandas as pd
# from Simulator import Simulator
# from investors_types.HumanHeuristicsInvestors import *
# from investors_types.PseudoAgents import *
# from investors_types.RLInvestor import RLInvestor
# import time
# from datetime import datetime
# from gym_simulator.envs.TrainerRL import TrainerRL
# from Config import *
#
# from tqdm import tqdm
#
# INITIAL_MONEY = 100000
#
#
# def get_columns_names():
#     return ['funds_this_run'] + [f'fund_q{i+1}' for i in range(43)] + [f'money_q{i}' for i in range(44)]
#
#
# def get_results_file_name(investor_type):
#     file_name = investor_type.__name__ + '_results '
#     now = datetime.now()
#     date_time = now.strftime("%d.%m.%Y %H-%M-%S")
#     file_name += date_time + '.csv'
#     return file_name
#
#
# def run_tests(n, investor_type, debug_mode=False):
#     print(f'Running {n} tests for {investor_type.__name__}...')
#     start_time = time.time()
#     df = pd.read_csv('funds_after_processing.csv')
#     results = []
#     funds_names = df['fund_symbol'].unique().tolist()
#     if investor_type == RLInvestor:
#         q_table = TrainerRL(max_episodes=NUM_OF_EPISODES).train()
#     else:
#         q_table = None
#     for _ in tqdm(range(n), desc="\tTesting Progress"):
#         sim = Simulator(df, INITIAL_MONEY, investor_type, debug_mode, funds_names, q_table)
#         result = sim.run_simulator()
#         results.append(result)
#     df = pd.DataFrame(results, columns=get_columns_names())
#     results_file_name = get_results_file_name(investor_type)
#     df.to_csv(results_file_name)
#     end_time = time.time()
#     print(f'\nFinished after {end_time - start_time} seconds.\nResults can be found in \'{results_file_name}\'')
#
#
# if __name__ == '__main__':
#     run_tests(NUM_OF_EXPERIMENTTS, RLInvestor, debug_mode=DEBUG_MODE)