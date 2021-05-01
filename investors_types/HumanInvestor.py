from investors_types.Investor import Investor


class HumanInvestor(Investor):

    def choose_fund(self, funds, year):
        # todo: must change or delete
        fund_symbols = [fund.get_symbol() for fund in funds]
        next_fund = input("Choose next fund ({}):\t".format(fund_symbols))
        # Getting fund by fund_symbol
        for fund in funds:
            if fund.get_symbol() == next_fund:
                return fund
