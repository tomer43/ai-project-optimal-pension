import pandas as pd
import random
from Fund import Fund
from Investor import Investor
from HumanInvestor import HumanInvestor
from AdminFeeInvestor import AdminFeeInvestor


def sample10Funds(df):
    funds = df['fund_symbol'].unique().tolist()
    selected_funds = random.sample(funds, 10)
    filtered_df = df[df['fund_symbol'].isin(selected_funds)]
    filtered_df.to_csv('sampled_funds.csv', index=False)
    return selected_funds


def createFunds():
    df = pd.read_csv('tmp_res_with_rolling.csv')
    funds = []
    fund_symbols = sample10Funds(df)
    num_of_cols = df.shape[1]

    for fund_symbol in fund_symbols:
        fund_df = df.loc[df['fund_symbol'] == fund_symbol]
        fund_details = []
        for col_num in range(num_of_cols):
            col = fund_df.iloc[:, col_num]
            if len(col.unique()) == 1 and col_num < 8:   # col_num < 8 because first 8 columns are properties of the fund, not properties of a queater, so they dont have to be represented as a list
                fund_details.append(col.iloc[0])
            else:
                fund_details.append(col.tolist())
        fund = Fund(fund_details)
        funds.append(fund)

    return funds


def makeInvestor(initial_money):
    # Here we choose the kind of agent
    return AdminFeeInvestor(initial_money)
    # return HumanInvestor(initial_money)
    # return Investor(initial_money)


class Simulator:
    def __init__(self, num_of_turns, initial_money):
        self.num_of_turns = num_of_turns
        self.investor = makeInvestor(initial_money)
        self.funds = createFunds()
        self.current_fund = None

    def runSimulator(self):
        turn = 0
        while turn < self.num_of_turns:
            self.current_fund = self.investor.choose_fund(self.funds, turn)
            turn += 1
            self.investor.update_money(self.current_fund, turn - 1)  # Updating money according to last quarter's performances

    def printFunds(self):
        print('*** ---------------------------------- Funds in current run ---------------------------------- ***\n')
        for f in self.funds:
            print(f)
        print('*** ------------------------------------------------------------------------------------------ ***')
        print('\n')

    def printFundSymbols(self):
        fund_symbols = [fund.getSymbol() for fund in self.funds]
        print('*** ------------------------------------ Funds in current run ------------------------------------ ***')
        print('\t', fund_symbols)
        print('*** ---------------------------------------------------------------------------------------------- ***')
        print('\n')

    def printResults(self):
        print('\n\n*** --------', type(self.investor).__name__, '-------- ***')
        print('\tInitial money:\t', self.investor.get_initial_money())
        print('\tFinal money:\t', self.investor.get_money())
        print('\tPROFIT = ', self.investor.get_money() - self.investor.get_initial_money())
        print('*** ---------------------------------- ***')


if __name__ == '__main__':
    sim = Simulator(num_of_turns=43, initial_money=100000)
    # sim.printFunds()
    sim.printFundSymbols()
    sim.runSimulator()
    sim.printResults()
