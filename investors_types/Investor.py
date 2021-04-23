import random


class Investor:
    def __init__(self, initial_money):
        self._initial_money = initial_money
        self._previous_money = initial_money
        self._current_money = initial_money

    def get_initial_money(self):
        return self._initial_money

    def get_money(self):
        return self._current_money

    def get_previous_money(self):
        return self._previous_money

    # Base class: choosing a fund randomly
    def choose_fund(self, funds, year):
        next_fund = random.choice(funds)
        # print('Investor: choose_fund:\t', next_fund.get_symbol())
        return next_fund
        # return random.choice(funds)

    def update_money(self, fund, quarter):
        self._previous_money = self._current_money
        rate = 1 + fund.get_returns()[quarter] / 100.0 - fund.get_admin_fees()[quarter] / 100.0
        self._current_money *= rate
        # print(f"{quarter}: {type(self).__name__}: {self._previous_money} --> {self._current_money}")
        # print(f"{quarter}: {self._previous_money} ---{fund.get_symbol()}---> {self._current_money}")