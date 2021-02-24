class Fund:
    def __init__(self, fund_details):
        self.fund_details = fund_details        # A dictionary containing all details of a fund (from CSV)

    def getSymbol(self):
        return self.fund_details['fund_symbol'][0]

    def getAdminFees(self):
        # return self.fund_net_annual_expense_ratio
        return self.fund_details['fund_quarterly_expense_ratio']

    def getReturns(self):
        return self.fund_details['fund_returns']

    def __str__(self):
        return str(self.fund_details)
