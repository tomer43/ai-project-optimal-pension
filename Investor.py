import random


class Investor:
    def __init__(self, initial_money):
        self.initial_money = initial_money
        self.current_money = initial_money

    def get_initial_money(self):
        return self.initial_money

    def get_money(self):
        return self.current_money

    # Base class: choosing a fund randomly
    def choose_fund(self, funds, year):
        next_fund = random.choice(funds)
        print('Investor: choose_fund:\t', next_fund.getSymbol())
        return next_fund
        # return random.choice(funds)

    def update_money(self, fund, quarter):
        # print('admin fee = {},   return = {}'.format(fund.getAdminFees()[quarter], fund.getReturns()[quarter]))
        rate = 1 + fund.getReturns()[quarter] / 100.0 - fund.getAdminFees()[quarter] / 100.0
        print('Quarter {}: {}'.format(quarter + 1, self.current_money * rate))  # 'quarter + 1' cuz money is calculated according to previous [quarter]
        self.current_money *= rate
