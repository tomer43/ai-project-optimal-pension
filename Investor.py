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
        print('Investor: choose_fund:\t', next_fund.getId())
        return next_fund
        # return random.choice(funds)

    def update_money(self, fund, year):
        rate = 1 + fund.getReturns()[year] / 100.0 - fund.getAdminFees()[year] / 100.0
        print(year + 1 + 2010, ' : ', self.current_money * rate)        # 2010 + 1 cuz money is calculated according to previous [year]
        self.current_money *= rate
