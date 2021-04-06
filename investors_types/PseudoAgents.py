from investors_types.Investor import Investor
import numpy as np
import random


class BestInvestor(Investor):
    def __init__(self, initial_money):
        super().__init__(initial_money)

    def choose_fund(self, funds, quarter):
        all_fund_returns = []
        for fund in funds:
            fund_return = fund.get_fund_param("fund_returns", quarter)
            fund_return -= fund.get_admin_fees_by_quarter(quarter)
            all_fund_returns.append(fund_return)
        best_fund_index = np.argmax(all_fund_returns)
        return funds[best_fund_index]


class WorstInvestor(Investor):
    def __init__(self, initial_money):
        super().__init__(initial_money)

    def choose_fund(self, funds, quarter):
        all_fund_returns = []
        for fund in funds:
            fund_return = fund.get_fund_param("fund_returns", quarter)
            fund_return -= fund.get_admin_fees_by_quarter(quarter)
            all_fund_returns.append(fund_return)
        best_fund_index = np.argmin(all_fund_returns)
        return funds[best_fund_index]


class MonkeyInvestor(Investor):
    def __init__(self, initial_money):
        super().__init__(initial_money)

    def choose_fund(self, funds, quarter):
        return random.sample(funds, 1)[0]
