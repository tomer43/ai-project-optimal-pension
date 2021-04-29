class Printer:
    @staticmethod
    def print_funds(simulator):
        print('*** ---------------------------------- Funds in current run ---------------------------------- ***\n')
        for fund in simulator.funds:
            print(fund)
        print('*** ------------------------------------------------------------------------------------------ ***')
        print('\n')

    @staticmethod
    def print_fund_symbols(simulator):
        fund_symbols = [fund.get_symbol() for fund in simulator.funds]
        print('*** ------------------------------------ Funds in current run ------------------------------------ ***')
        print('\t', fund_symbols)
        print('*** ---------------------------------------------------------------------------------------------- ***')
        print('\n')

    @staticmethod
    def print_final_results(investor):
        print(f'\n\n*** ----------- {type(investor).__name__} ----------- ***')
        print(f'\n\tInitial money:\t{investor.get_initial_money()}')
        print(f'\tFinal money:\t{investor.get_money()}')
        print(f'\n\tProfit = {round(((investor.get_money() / investor.get_initial_money()) * 100), 2)}% ({investor.get_money() - investor.get_initial_money()})')
        print('\n*** ----------------------------------------- ***')

    @staticmethod
    def print_results_path(results_line):
        funds_in_run = results_line[0]
        funds = results_line[1:44]
        sums = [str(x) for x in results_line[44:88]]
        print('\nFunds in current run:  ', funds_in_run + '\n')
        print('\t' + ' --> '.join(funds))
        print('\t' + ' --> '.join(sums))
