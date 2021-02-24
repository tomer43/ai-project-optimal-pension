import pandas as pd
import random
from Fund import Fund
from Investor import Investor
from HumanInvestor import HumanInvestor
from AdminFeeInvestor import AdminFeeInvestor

NUM_OF_TURNS = 43


def sample10Funds(df):
    funds = df['fund_symbol'].unique().tolist()
    selected_funds = random.sample(funds, 10)
    return selected_funds


def createFunds():
    df = pd.read_csv('funds_after_processing.csv')
    funds = []
    selected_funds = sample10Funds(df)
    # selected_funds = ['AAAAX', 'AAAGX', 'AAAIX', 'AAAPX', 'AAARX', 'AAASX', 'AAATX', 'AAAZX', 'AABCX', 'AABFX'] # RL funds
    # selected_funds = ['NBHIX', 'ACFCX', 'IAAAX', 'QBNAX', 'WESCX', 'MDVYX', 'RCMFX', 'MSXAX', 'HRCPX', 'FLRLX']
    for fund_symbol in selected_funds:
        fund_df = df[df['fund_symbol'] == fund_symbol]
        fund_details = fund_df.to_dict('list')
        fund = Fund(fund_details)
        funds.append(fund)
    return funds


class Simulator:
    def __init__(self, initial_money, investor):
        # self.num_of_turns = num_of_turns
        self.investor = investor(initial_money)
        self.funds = createFunds()
        self.current_fund = None

    def runSimulator(self):
        turn = 0
        while turn < NUM_OF_TURNS:
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
    sim = Simulator(initial_money=100000, investor=AdminFeeInvestor)
    # sim.printFunds()
    sim.printFundSymbols()
    sim.runSimulator()
    sim.printResults()
