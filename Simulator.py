import pandas as pd
import random
from Fund import Fund
from Printer import *
from investors_types.HumanHeuristicsInvestors import *
from investors_types.HumanInvestor import HumanInvestor
from investors_types.PseudoAgents import *
from investors_types.RLInvestor import RLInvestor
from Config import *


INITIAL_MONEY = 100000
NUM_OF_TURNS = 43


def sample_funds(funds):
    selected_funds = random.sample(funds, NUM_OF_FUNDS)
    return selected_funds


def create_funds(df, debug_mode, funds_names):
    funds = []
    if debug_mode:
        # selected_funds = ['AAAAX', 'AAAGX', 'AAAIX', 'AAAPX', 'AAARX', 'AAASX', 'AAATX', 'AAAZX', 'AABCX', 'AABFX']
        selected_funds = funds_names[:NUM_OF_FUNDS]
    else:
        selected_funds = sample_funds(funds_names)
    selected_fund_df = df.loc[df['fund_symbol'].isin(selected_funds)]
    for fund_symbol in selected_funds:
        fund_details = selected_fund_df.loc[selected_fund_df['fund_symbol'] == fund_symbol].to_dict('list')
        fund = Fund(fund_details)
        funds.append(fund)
    return funds


class Simulator:
    def __init__(self, df, initial_money, investor, debug_mode=False, funds_names=None, q_table=None):
        if investor != RLInvestor:
            self._investor = investor(initial_money)
        else:
            self._investor = investor(initial_money, q_table)
        if funds_names is None:
            funds_names = df['fund_symbol'].unique().tolist()
        self._funds = create_funds(df, debug_mode, funds_names)
        self._current_fund = None

    def get_investor(self):
        return self._investor

    def run_simulator(self):
        turn = 0
        funds_in_this_run = ', '.join([fund.get_symbol() for fund in self._funds])
        funds_by_quarters , money_by_quarter = [], [self._investor.get_initial_money()]
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
    sim = Simulator(funds_csv, initial_money=INITIAL_MONEY, investor=LowestFeeInvestor, debug_mode=DEBUG_MODE)
    # Printer.print_funds(sim)
    # Printer.print_fund_symbols(sim)
    results_line = sim.run_simulator()
    Printer.print_results_path(results_line)
    Printer.print_final_results(sim)







# ---------------------------------------------------------------------------------
# import pandas as pd
# import random
# from Fund import Fund
# from Printer import *
# from investors_types.HumanHeuristicsInvestors import *
# from investors_types.HumanInvestor import HumanInvestor
# from investors_types.PseudoAgents import *
# from investors_types.RLInvestor import RLInvestor
# from Config import *
#
#
# INITIAL_MONEY = 100000
# NUM_OF_TURNS = 43
#
#
# def sample_funds(funds):
#     selected_funds = random.sample(funds, NUM_OF_FUNDS)
#     return selected_funds
#
#
# def create_funds(df, debug_mode, funds_names):
#     funds = []
#     if debug_mode:
#         # selected_funds = ['AAAAX', 'AAAGX', 'AAAIX', 'AAAPX', 'AAARX', 'AAASX', 'AAATX', 'AAAZX', 'AABCX', 'AABFX']
#         selected_funds = funds_names[:NUM_OF_FUNDS]
#     else:
#         selected_funds = sample_funds(funds_names)
#     selected_fund_df = df.loc[df['fund_symbol'].isin(selected_funds)]
#     for fund_symbol in selected_funds:
#         fund_details = selected_fund_df.loc[selected_fund_df['fund_symbol'] == fund_symbol].to_dict('list')
#         fund = Fund(fund_details)
#         funds.append(fund)
#     return funds
#
#
# class Simulator:
#     def __init__(self, df, initial_money, investor, debug_mode=False, funds_names=None, q_table=None):
#         if investor != RLInvestor:
#             self._investor = investor(initial_money)
#         else:
#             self._investor = investor(initial_money, q_table)
#         if funds_names is None:
#             funds_names = df['fund_symbol'].unique().tolist()
#         self._funds = create_funds(df, debug_mode, funds_names)
#         self._current_fund = None
#
#     def get_investor(self):
#         return self._investor
#
#     def run_simulator(self):
#         turn = 0
#         funds_in_this_run = ', '.join([fund.get_symbol() for fund in self._funds])
#         funds_by_quarters , money_by_quarter = [], [self._investor.get_initial_money()]
#         while turn < NUM_OF_TURNS:
#             self._current_fund = self._investor.choose_fund(self._funds, turn)
#             funds_by_quarters.append(self._current_fund.get_symbol())
#             turn += 1
#
#             # Updating money according to last quarter's performances
#             self._investor.update_money(self._current_fund, turn - 1)
#             money_by_quarter.append(self._investor.get_money())
#         res = [funds_in_this_run] + funds_by_quarters + money_by_quarter
#         return res
#
#
# if __name__ == '__main__':
#     funds_csv = pd.read_csv('funds_after_processing.csv')
#     sim = Simulator(funds_csv, initial_money=INITIAL_MONEY, investor=LowestFeeInvestor, debug_mode=DEBUG_MODE)
#     # Printer.print_funds(sim)
#     # Printer.print_fund_symbols(sim)
#     results_line = sim.run_simulator()
#     Printer.print_results_path(results_line)
#     Printer.print_final_results(sim)