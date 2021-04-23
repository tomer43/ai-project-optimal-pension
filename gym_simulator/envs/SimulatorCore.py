# https://github.com/monokim/framework_tutorial


import pandas as pd
import random
from Fund import Fund
from gym_simulator.envs.State import State
from Printer import *

cached_funds = {}


def sample_10_funds(funds):
    selected_funds = random.sample(funds, 10)
    return selected_funds


def create_funds(df, debug_mode, funds_names):
    funds = []
    if debug_mode:
        selected_funds = ['AAAAX', 'AAAGX', 'AAAIX', 'AAAPX', 'AAARX', 'AAASX', 'AAATX', 'AAAZX', 'AABCX', 'AABFX']
    else:
        selected_funds = sample_10_funds(funds_names)

    uncached_funds = list(set(selected_funds) - set(cached_funds.keys()))
    if uncached_funds:
        selected_fund_df = df.loc[uncached_funds]
        for fund_symbol in uncached_funds:
            fund_details = selected_fund_df.loc[fund_symbol].to_dict('list')
            fund_details['fund_symbol'] = [fund_symbol] * len(fund_details['ts'])
            fund = Fund(fund_details)
            cached_funds[fund_symbol] = fund

    for fund_symbol in selected_funds:
        funds.append(cached_funds[fund_symbol])

    return funds


class SimulatorCore:
    def __init__(self, df, investor, debug_mode=False, funds_names=None):
        self._investor = investor
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

    def get_funds(self):
        return self._funds

    def get_funds_symbol(self):
        funds_in_this_run = ', '.join([fund.get_symbol() for fund in self._funds])
        return funds_in_this_run

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
        # s = State(self._funds, self._turn)
        # return s.get_state()
        return State.get_state_with_no_object_creation(self._funds, self._turn)

    def evaluate(self):
        return self._investor.get_money() - self._investor.get_previous_money()

    def is_done(self):
        if self._turn == 43:
            return True
        else:
            return False

    def view(self):
        pass