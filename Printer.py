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
    def print_final_results(simulator):
        print('\n\n*** --------', type(simulator.get_investor()).__name__, '-------- ***')
        print('\tInitial money:\t', simulator.get_investor().get_initial_money())
        print('\tFinal money:\t', simulator.get_investor().get_money())
        print('\tPROFIT = ', simulator.get_investor().get_money() - simulator.get_investor().get_initial_money())
        print('*** ---------------------------------- ***')

    @staticmethod
    def print_results_path(results_line):
        funds_in_run = results_line[0]
        funds = results_line[1:44]
        sums = [str(x) for x in results_line[44:88]]
        print('\nFunds in current run:  ', funds_in_run + '\n')
        print('\t' + ' --> '.join(funds))
        print('\t' + ' --> '.join(sums))