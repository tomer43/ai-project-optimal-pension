class Fund:
    def __init__(self, fund_info):
        self._fund_info = fund_info       # fund_info = A dictionary containing all details of a fund (from CSV)

    def get_symbol(self):
        return self._fund_info['fund_symbol'][0]

    def get_admin_fees(self):
        return self._fund_info['fund_quarterly_expense_ratio']

    def get_admin_fees_by_quarter(self, quarter):
        return self._fund_info['fund_quarterly_expense_ratio'][quarter]

    def get_returns(self):
        return self._fund_info['fund_returns']

    def get_fund_info(self):
        return self._fund_info

    def get_fund_param(self, param_name, quarter_index):
        if param_name not in self._fund_info.keys():
            raise ValueError("Invalid param_name")
        if quarter_index not in range(0, 43):
            raise ValueError("Invalid quarter_index")
        return self._fund_info[param_name][quarter_index]

    def __str__(self):
        return str(self._fund_info)
