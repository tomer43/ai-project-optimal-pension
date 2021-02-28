class Fund:
    def __init__(self, fund_info):
        self._fund_info = fund_info       # fund_info = A dictionary containing all details of a fund (from CSV)

    def get_symbol(self):
        return self._fund_info['fund_symbol'][0]

    def get_admin_fees(self):
        return self._fund_info['fund_quarterly_expense_ratio']

    def get_returns(self):
        return self._fund_info['fund_returns']

    def get_fund_info(self):
        return self._fund_info

    def __str__(self):
        return str(self._fund_info)
