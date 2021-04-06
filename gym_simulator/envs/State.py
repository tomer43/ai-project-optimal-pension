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
        self._admin_fees = get_funds_param_by_quarter(funds, 'fund_quarterly_expense_ratio', turn)
        # self._healthcare = get_funds_param_by_quarter(funds, 'sector_healthcare', turn)

    def get_state(self):
        return (self._admin_fees)
        # return (self._admin_fees, self._healthcare)
