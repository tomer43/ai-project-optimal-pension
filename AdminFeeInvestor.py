from Investor import Investor
import numpy as np


class AdminFeeInvestor(Investor):
    def choose_fund(self, funds, quarter):
        fees_this_quarter = []
        for fund in funds:
            fees_this_quarter.append(fund.get_admin_fees()[quarter])
        cheapest_fund_index = np.argmin(fees_this_quarter)
        return funds[cheapest_fund_index]
