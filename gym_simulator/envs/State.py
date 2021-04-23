def get_funds_param_by_quarter(funds, param_name, quarter_idx):
    if quarter_idx == 43:
        return (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    else:
        funds_params_by_quarter = []
        for fund in funds:
            # funds_params_by_quarter.append(fund.get_fund_param(param_name, quarter_idx))
            funds_params_by_quarter.append( round(fund.get_fund_param(param_name, quarter_idx), 1) )

            # funds_params_by_quarter.append(round(fund.get_fund_param(param_name, quarter_idx), 2))

        return tuple(funds_params_by_quarter)


class State:
    def __init__(self, funds, turn):
        self._admin_fees = get_funds_param_by_quarter(funds, 'fund_quarterly_expense_ratio', turn)
        self._last_five_years_reuturns = get_funds_param_by_quarter(funds, 'fund_total_last_5_years_returns', turn)
        self._technology = get_funds_param_by_quarter(funds, 'sector_technology', turn)


    def get_state(self):
        # return (self._admin_fees)
        return (self._admin_fees, self._last_five_years_reuturns, self._technology)