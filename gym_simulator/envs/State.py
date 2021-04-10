import pandas as pd


def get_funds_param_by_quarter(funds, param_name, quarter_idx):
    if quarter_idx == 43:
        return (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    else:
        funds_params_by_quarter = []
        for fund in funds:
            funds_params_by_quarter.append(fund.get_fund_param(param_name, quarter_idx))
        return tuple(funds_params_by_quarter)


class State:
    def __init__(self, funds, turn):
        params = ['fund_last_quarter_returns', 'fund_total_last_year_returns',
                  'fund_total_last_3_years_returns', 'fund_total_last_5_years_returns', 'fund_quarterly_expense_ratio']
        self._state_parameters = pd.DataFrame(index=params, data=0, columns=[i for i in range(10)])
        for par in params:
            self._state_parameters.loc[par] = get_funds_param_by_quarter(funds, par, turn)

    def get_state(self):
        return self._state_parameters
