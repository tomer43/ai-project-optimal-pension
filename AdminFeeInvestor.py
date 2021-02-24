from Investor import Investor
import numpy as np


class AdminFeeInvestor(Investor):
    def choose_fund(self, funds, quarter):
        fees_this_quarter = []
        for fund in funds:
            fees_this_quarter.append(fund.getAdminFees()[quarter])
        cheapest_fund_index = np.argmin(fees_this_quarter)
        # print('Chose fund {}'.format( (funds[cheapest_fund_index].getSymbol())  ))
        return funds[cheapest_fund_index]
