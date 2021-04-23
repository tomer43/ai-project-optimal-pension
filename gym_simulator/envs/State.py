import numpy as np
import pandas as pd


def get_funds_param_by_quarter(funds, param_name, quarter_idx):
    if quarter_idx == 43:
        return (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    else:
        funds_params_by_quarter = [0] * 10
        for i, fund in enumerate(funds):
            funds_params_by_quarter[i] = fund.get_fund_param(param_name, quarter_idx)
        return tuple(funds_params_by_quarter)


class State:
    def __init__(self, funds, turn):
        state_info = ['fund_total_last_5_years_returns',
                      'fund_total_last_3_years_returns',
                      'fund_total_last_year_returns',
                      'fund_last_quarter_returns',
                      'fund_quarterly_expense_ratio',
                      'asset_stocks',
                      'asset_bonds',
                      'asset_cash',
                      'asset_others']
        self._state_parameters = np.ndarray((10, 9))
        for i, param in enumerate(state_info, start=0):
            self._state_parameters[:, i] = get_funds_param_by_quarter(funds, param, turn)

    def get_state(self):
        return self._state_parameters

    @staticmethod
    def get_state_with_no_object_creation(funds, turn):
        state_info = ['fund_total_last_5_years_returns',
                      'fund_total_last_3_years_returns',
                      'fund_total_last_year_returns',
                      'fund_last_quarter_returns',
                      'fund_quarterly_expense_ratio',
                      'asset_stocks',
                      'asset_bonds',
                      'asset_cash',
                      'asset_others']
        state_parameters = np.ndarray((10, 9))
        for i, param in enumerate(state_info, start=0):
            state_parameters[:, i] = get_funds_param_by_quarter(funds, param, turn)
        return state_parameters