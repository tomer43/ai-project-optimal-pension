import pandas as pd
from Fund import Fund
from Investor import Investor
from HumanInvestor import HumanInvestor
from AdminFeeInvestor import AdminFeeInvestor


def getFunds():
    df = pd.read_csv('mutual_funds_toy_example.csv')
    # df = df.sample(n=10)      # Uncomment when using final csv

    returns_df = df.loc[:, 'fund_return_2019':'fund_return_2010']
    returns_list = returns_df.values.tolist()
    returns_rev_list = [x[::-1] for x in returns_list]

    admin_fees_df = df.loc[:, 'fees_2019':'fees_2010']
    admin_fees_list = admin_fees_df.values.tolist()
    admin_fees_rev_list = [x[::-1] for x in admin_fees_list]

    funds = []
    for index in range(len(admin_fees_rev_list)):
        admin_fees = admin_fees_rev_list[index]
        returns = returns_rev_list[index]
        fund = Fund(index + 1, admin_fees, returns)
        funds.append(fund)
    return funds


def makeInvestor(initial_money):
    return AdminFeeInvestor(initial_money)  # Here we choose the kind of agent


class Simulator:
    def __init__(self, num_of_turns, initial_money):
        self.num_of_turns = num_of_turns
        self.investor = makeInvestor(initial_money)
        self.funds = getFunds()
        self.current_fund = None

    def runSimulator(self):
        turn = 0
        while turn < self.num_of_turns:
            self.current_fund = self.investor.choose_fund(self.funds, turn)
            turn += 1
            self.investor.update_money(self.current_fund, turn - 1)  # Updating money according to last year's performances

    def printFunds(self):
        for f in self.funds:
            print(f)
        print()

    def printResults(self):
        print('\n\n*** --------', type(self.investor).__name__, '-------- ***')
        print('\tInitial money:\t', self.investor.get_initial_money())
        print('\tFinal money:\t', self.investor.get_money())
        print('\tPROFIT = ', self.investor.get_money() - self.investor.get_initial_money())
        print('*** ---------------------------------- ***')


if __name__ == '__main__':
    sim = Simulator(num_of_turns=10, initial_money=100000)
    sim.printFunds()
    sim.runSimulator()
    sim.printResults()
