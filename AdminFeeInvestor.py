from Investor import Investor
import numpy as np


class AdminFeeInvestor(Investor):
    def choose_fund(self, funds, year):
        fees_this_year = []
        for fund in funds:
            fees_this_year.append(fund.getAdminFees()[year])
        cheapest_fund_index = np.argmin(fees_this_year)
        return funds[cheapest_fund_index]
