import pandas as pd
import random
from Fund import Fund
from investors_types.HumanHeuristicsInvestors import *
from Printer import *

NUM_OF_TURNS = 43


def sample_10_funds(df):
    funds = df['fund_symbol'].unique().tolist()
    selected_funds = random.sample(funds, 10)
    return selected_funds


def create_funds(df, debug_mode):
    funds = []
    if debug_mode:
        selected_funds = ['AAAAX', 'AAAGX', 'AAAIX', 'AAAPX', 'AAARX', 'AAASX', 'AAATX', 'AAAZX', 'AABCX', 'AABFX']
    else:
        selected_funds = sample_10_funds(df)
    for fund_symbol in selected_funds:
        fund_df = df[df['fund_symbol'] == fund_symbol]
        fund_details = fund_df.to_dict('list')
        fund = Fund(fund_details)
        funds.append(fund)
    return funds


class Simulator:
    def __init__(self, df, initial_money, investor, debug_mode=False):
        self._investor = investor(initial_money)
        self._funds = create_funds(df, debug_mode)
        self._current_fund = None

    def get_investor(self):
        return self._investor

    def run_simulator(self):
        turn = 0
        funds_in_this_run = ', '.join([fund.get_symbol() for fund in self._funds])
        funds_by_quarters, money_by_quarter = [], []
        while turn < NUM_OF_TURNS:
            self._current_fund = self._investor.choose_fund(self._funds, turn)
            funds_by_quarters.append(self._current_fund.get_symbol())
            turn += 1

            # Updating money according to last quarter's performances
            self._investor.update_money(self._current_fund, turn - 1)
            money_by_quarter.append(self._investor.get_money())
        res = [funds_in_this_run] + funds_by_quarters + money_by_quarter
        return res


if __name__ == '__main__':
    funds_csv = pd.read_csv('funds_after_processing.csv')
    sim = Simulator(funds_csv, initial_money=100000, investor=LargestFundInvestor, debug_mode=True)
    # Printer.print_funds(sim)
    # Printer.print_fund_symbols(sim)
    results_line = sim.run_simulator()
    Printer.print_results_path(results_line, sim.get_investor().get_initial_money())
    Printer.print_final_results(sim)
