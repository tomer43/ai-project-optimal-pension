import random

import numpy as np

from investors_types.Investor import Investor


class BestInvestor(Investor):
    def __init__(self, initial_money):
        super().__init__(initial_money)

    def choose_fund(self, state):
        fund_returns = state[:, self._features_idx['fund_returns']]
        funds_expense_ratio = state[:, self._features_idx['fund_quarterly_expense_ratio']]
        return np.argmax(fund_returns - funds_expense_ratio)


class WorstInvestor(Investor):
    def __init__(self, initial_money):
        super().__init__(initial_money)

    def choose_fund(self, state):
        fund_returns = state[:, self._features_idx['fund_returns']]
        funds_expense_ratio = state[:, self._features_idx['fund_quarterly_expense_ratio']]
        return np.argmin(fund_returns - funds_expense_ratio)


class MonkeyInvestor(Investor):
    def __init__(self, initial_money):
        super().__init__(initial_money)

    def choose_fund(self, state):
        return random.randint(0, 9)
