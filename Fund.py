class Fund:
    def __init__(self, fund_details):
        self.fund_details = fund_details       # fund_details = A dictionary containing all details of a fund (from CSV)

    def get_symbol(self):
        return self.fund_details['fund_symbol'][0]

    def get_admin_fees(self):
        return self.fund_details['fund_quarterly_expense_ratio']

    def get_returns(self):
        return self.fund_details['fund_returns']

    def __str__(self):
        return str(self.fund_details)
