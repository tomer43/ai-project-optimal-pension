from Investor import Investor
from HumanInvestor import HumanInvestor
from Fund import Fund
import random


# TODO: re-implement this using the post-process CSV (instead of random values): update Fund object fields, create a list of Fund objects and return it
def getFunds():
    funds = []
    for index in range(10):
        admin_fees = random.sample(range(10, 100), 10)
        returns = random.sample(range(100, 1000), 10)
        fund = Fund(index + 1, admin_fees, returns)
        funds.append(fund)
    return funds


def makeInvestor(initial_money):
    return HumanInvestor(initial_money)


class Simulator:
    def __init__(self, num_of_turns, initial_money):
        self.num_of_turns = num_of_turns
        self.investor = makeInvestor(initial_money)
        self.funds = getFunds()
        self.current_fund = None

    def runSimulator(self):
        turn = 0
        self.current_fund = self.investor.choose_fund(self.funds)  # Choosing starting fund
        while turn != self.num_of_turns:
            turn += 1
            self.investor.update_money(self.current_fund, turn - 1)  # Updating money according to last year's performances
            self.current_fund = self.investor.choose_fund(self.funds)
        self.investor.update_money(self.current_fund, turn - 1)

    def printFunds(self):
        for f in self.funds:
            print(f)

    def printResults(self):
        print('\n-----------------------')
        print('Initial money:\t', self.investor.get_initial_money())
        print('Final money:\t', self.investor.get_money())
        print('PROFIT = ', self.investor.get_money() - self.investor.get_initial_money())


if __name__ == '__main__':
    sim = Simulator(num_of_turns=10, initial_money=100000)
    sim.printFunds()
    sim.runSimulator()
    sim.printResults()
    # print('DONE')
