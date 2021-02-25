import pandas as pd
import random
from Fund import Fund
from Investor import Investor
from HumanInvestor import HumanInvestor
from AdminFeeInvestor import AdminFeeInvestor
from Printer import *

NUM_OF_TURNS = 43


def sample_10_funds(df):
    funds = df['fund_symbol'].unique().tolist()
    selected_funds = random.sample(funds, 10)
    return selected_funds


def create_funds():
    df = pd.read_csv('funds_after_processing.csv')
    funds = []
    # selected_funds = sample_10_funds(df)
    selected_funds = ['AAAAX', 'AAAGX', 'AAAIX', 'AAAPX', 'AAARX', 'AAASX', 'AAATX', 'AAAZX', 'AABCX', 'AABFX']  # RL funds
    # selected_funds = ['NBHIX', 'ACFCX', 'IAAAX', 'QBNAX', 'WESCX', 'MDVYX', 'RCMFX', 'MSXAX', 'HRCPX', 'FLRLX']
    for fund_symbol in selected_funds:
        fund_df = df[df['fund_symbol'] == fund_symbol]
        fund_details = fund_df.to_dict('list')
        fund = Fund(fund_details)
        funds.append(fund)
    return funds


class Simulator:
    def __init__(self, initial_money, investor):
        self.investor = investor(initial_money)
        self.funds = create_funds()
        self.current_fund = None

    def run_simulator(self):
        turn = 0
        funds_in_this_run = ', '.join([fund.get_symbol() for fund in self.funds])
        funds_by_quarters , money_by_quarter = [], []
        while turn < NUM_OF_TURNS:
            self.current_fund = self.investor.choose_fund(self.funds, turn)
            funds_by_quarters.append(self.current_fund.get_symbol())
            turn += 1
            self.investor.update_money(self.current_fund, turn - 1)  # Updating money according to last quarter's performances
            money_by_quarter.append(self.investor.get_money())
        res = [funds_in_this_run] + funds_by_quarters + money_by_quarter
        return res


if __name__ == '__main__':
    sim = Simulator(initial_money=100000, investor=AdminFeeInvestor)
    # Printer.print_funds(sim)
    # Printer.print_fund_symbols(sim)
    results_line = sim.run_simulator()
    Printer.print_results_path(results_line, sim.investor.get_initial_money())
    Printer.print_final_results(sim)
