import random
from our_simulator.State import get_state_features_to_idx


class Investor:
    def __init__(self, initial_money, **kwargs):
        self._initial_money = initial_money
        self._previous_money = initial_money
        self._current_money = initial_money
        self._features_idx = get_state_features_to_idx()

    def get_initial_money(self):
        return self._initial_money

    def get_money(self):
        return self._current_money

    def get_previous_money(self):
        return self._previous_money

    # Base class: choosing a fund randomly
    def choose_fund(self, state):
        next_fund_idx = random.randint(0, 9)
        return next_fund_idx

    def update_money(self, fund, quarter):
        self._previous_money = self._current_money
        rate = 1 + fund.get_returns()[quarter] / 100.0 - fund.get_admin_fees()[quarter] / 100.0
        self._current_money *= rate

    def reset_money(self):
        self._previous_money = self._initial_money
        self._current_money = self._initial_money
