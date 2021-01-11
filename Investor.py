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
    def choose_fund(self, funds):
        next_fund = random.choice(funds)
        print('Investor: choose_fund:\t', next_fund.getId())
        return next_fund
        # return random.choice(funds)


    def update_money(self, fund, year):
        self.current_money = self.current_money + (fund.getReturns())[year]