class Fund:
    def __init__(self, id, administration_fees, returns):
        self.id = id
        self.administration_fees = administration_fees  # list with [number of periods] administration fees
        self.returns = returns     # list with [number of periods] returns

    def getId(self):
        return self.id

    def getAdminFees(self):
        return self.administration_fees

    def getReturns(self):
        return self.returns

    def __str__(self):
        fund_str = 'fund ' + str(self.id) + ':\n'
        fund_str += '\t' + 'Administration fees:\t' + str(self.administration_fees) +'\n'
        fund_str += '\t' + 'Returns:\t' + str(self.returns)
        fund_str += '\n'
        return fund_str

