# https://github.com/monokim/framework_tutorial


import pandas as pd
import random
from Fund import Fund
from gym_simulator.envs.State import State
from investors_types.HumanHeuristicsInvestors import *
from investors_types.PseudoAgents import *
from Printer import *

NUM_OF_TURNS = 43

# actions = [LowestFeeInvestor]
actions = [BestReturnLastQuarterInvestor, BestReturnLastYearInvestor, BestReturnLastThreeYearsInvestor,
           BestReturnLastFiveYearsInvestor, TechnologyInvestor, RealEstateInvestor,
           LargestFundInvestor, ExpertAdviceInvestor, LowestFeeInvestor]


def sample_10_funds(funds):
    selected_funds = random.sample(funds.tolist(), 10)
    return selected_funds


def create_funds(df, debug_mode, funds_names):
    funds = []
    if debug_mode:
        selected_funds = ['AAAAX', 'AAAGX', 'AAAIX', 'AAAPX', 'AAARX', 'AAASX', 'AAATX', 'AAAZX', 'AABCX', 'AABFX']
    else:
        selected_funds = sample_10_funds(funds_names)
    selected_fund_df = df.loc[df['fund_symbol'].isin(selected_funds)]
    for fund_symbol in selected_funds:
        fund_details = selected_fund_df.loc[selected_fund_df['fund_symbol'] == fund_symbol].to_dict('list')
        fund = Fund(fund_details)
        funds.append(fund)
    return funds


class SimulatorRL:
    def __init__(self, df, initial_money, investor, debug_mode=False, funds_names=None):
        self._investor = investor(initial_money)
        if funds_names is None:
            funds_names = df['fund_symbol'].unique()
        self._funds = create_funds(df, debug_mode, funds_names)
        self._current_fund = None
        self._turn = 0

    def set_investor(self, investor_type, money):
        self._investor = investor_type(money)

    def get_funds_param_by_quarter(self, param_name, quarter_idx):
        funds_params_by_quarter = []
        for fund in self._funds:
            funds_params_by_quarter.append(fund.get_fund_param(param_name, quarter_idx))
        return funds_params_by_quarter

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Q-learning stuff ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def action(self, action):
        # investor_type = actions[action]
        # self.set_investor(investor_type, self._investor.get_money())
        # self._current_fund = self._investor.choose_fund(self._funds, self._turn)
        fund = self._funds[action]
        self._current_fund = fund
        self._investor.update_money(fund, self._turn)
        # print(f"{self._turn}: {self._investor.get_previous_money()} --{action}--> {self._investor.get_money()}")
        self._turn += 1

    def observe(self):
        s = State(self._funds, self._turn)
        return s.get_state()

    def evaluate(self):
        return self._investor.get_money() - self._investor.get_previous_money()

    def is_done(self):
        if self._turn == 43:
            return True
        else:
            return False

    def view(self):
        pass
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# -------------------------------------------------------------------------------

# import pandas as pd
# import random
# from Fund import Fund
# from gym_simulator.envs.InvestorRL import InvestorRL
#
#
# def sample10Funds(df):
#     funds = df['fund_symbol'].unique().tolist()
#     selected_funds = random.sample(funds, 10)
#     filtered_df = df[df['fund_symbol'].isin(selected_funds)]
#     filtered_df.to_csv('sampled_funds.csv', index=False)
#     return selected_funds
#
#
# def createFunds():
#     # df = pd.read_csv('tmp_res_with_rolling.csv')
#     df = pd.read_csv('funds_after_processing.csv')
#     funds = []
#     # fund_symbols = sample10Funds(df)
#     fund_symbols = ['AAAAX', 'AAAGX', 'AAAIX', 'AAAPX', 'AAARX', 'AAASX', 'AAATX', 'AAAZX', 'AABCX', 'AABFX']
#     num_of_cols = df.shape[1]
#
#     for fund_symbol in fund_symbols:
#         fund_df = df.loc[df['fund_symbol'] == fund_symbol]
#         fund_details = []
#         for col_num in range(num_of_cols):
#             col = fund_df.iloc[:, col_num]
#             if len(
#                     col.unique()) == 1 and col_num < 8:  # col_num < 8 because first 8 columns are properties of the fund, not properties of a queater, so they dont have to be represented as a list
#                 fund_details.append(col.iloc[0])
#             else:
#                 fund_details.append(col.tolist())
#         fund = Fund(fund_details)
#         funds.append(fund)
#
#     print('*** ------------------------------------ Funds in current run ------------------------------------ ***')
#     print('\t', fund_symbols)
#     print('*** ---------------------------------------------------------------------------------------------- ***')
#     return funds
#
#
# def makeInvestor(initial_money):
#     return InvestorRL(initial_money)
#
#
# class SimulatorRL:
#     def __init__(self, num_of_turns, initial_money):
#         self._num_of_turns = num_of_turns
#         self._investor = makeInvestor(initial_money)
#         self._funds = createFunds()
#         self._current_fund = None
#
#
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Q-learning stuff ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     def action(self, action):
#             # self.investor.update_money(self.funds, action)
#         self._investor.update_money(self._current_fund, self._investor.get_turn() - 1)
#         self.current_fund = action
#
#     def observe(self):
#         return int(self._investor.get_money())
#         # return int(self.investor.get_money()) - (int(self.investor.get_money()) % 10)
#
#     def evaluate(self):
#         return self._investor.get_money() - self._investor.get_previous_money()
#
#     def is_done(self):
#         if self._investor.turn == 43:
#             return True
#         else:
#             return False
#
#     def view(self):
#         pass
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
