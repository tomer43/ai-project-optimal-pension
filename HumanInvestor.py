from Investor import Investor

class HumanInvestor(Investor):

    def choose_fund(self, funds):
        next_fund = input("Choose next fund (1-{}):\t".format(len(funds)))
        return funds[int(next_fund) - 1]