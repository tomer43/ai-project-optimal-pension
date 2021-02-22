from Investor import Investor

class HumanInvestor(Investor):

    def choose_fund(self, funds, year):
        fund_symbols = [fund.getSymbol() for fund in funds]
        next_fund = input("Choose next fund ({}):\t".format(fund_symbols))
        # Getting fund by fund_symbol
        for fund in funds:
            if fund.getSymbol() == next_fund:
                return fund
