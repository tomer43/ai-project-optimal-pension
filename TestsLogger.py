import pandas as pd
from Simulator import Simulator
from Investor import Investor
from HumanInvestor import HumanInvestor
from AdminFeeInvestor import AdminFeeInvestor
import time

INITIAL_MONEY = 100000


def get_columns_names():
    cols = []
    cols.append('funds_this_run')
    for i in range(43):
        cols.append('fund_q' + str(i + 1))
    for i in range(43):
        cols.append('money_q' + str(i + 1))
    return cols


def run_tests(n, investor_type):
    print('Running {} tests for {}...\n'.format(n, investor_type.__name__))
    start_time = time.time()
    results = []
    for i in range(n):
        sim = Simulator(INITIAL_MONEY, investor_type)
        result = sim.run_simulator()
        results.append(result)
    df = pd.DataFrame(results, columns=get_columns_names())
    df.to_csv('test_results.csv')
    end_time = time.time()
    print('Finished after {} seconds.\nResults can be found in \'test_results.csv\''.format(end_time - start_time))


if __name__ == '__main__':
    run_tests(100, AdminFeeInvestor)