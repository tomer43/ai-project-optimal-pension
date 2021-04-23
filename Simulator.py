import pandas as pd
from Printer import *
from gym_simulator.envs.custom_env import CustomEnv
from investors_types.HumanHeuristicsInvestors import *
from investors_types.HumanInvestor import HumanInvestor
from investors_types.PseudoAgents import *
from investors_types.RLInvestor import RLInvestor


class Simulator:
    def __init__(self, funds_csv, funds_list_names, investor, investor_kwargs=None):
        self._env = CustomEnv(funds_csv, funds_list_names, investor, investor_kwargs)

    def run_simulator(self):
        funds_in_this_run = self._env.get_funds_in_this_run()
        funds_by_quarters, money_by_quarter = [], [self._env.get_investor_money()]

        done = False
        initial_state = self._env.reset()
        curr_state = initial_state
        while not done:
            action = self._env.investor_action(curr_state)
            next_state, reward, done, _ = self._env.step(action)
            curr_state = next_state
            funds_by_quarters.append(action)
            money_by_quarter.append(self._env.get_investor_money())

        res = [funds_in_this_run] + funds_by_quarters + money_by_quarter
        return res


if __name__ == '__main__':
    # funds_csv = pd.read_csv('funds_after_processing.csv')
    # rl_investor_args = {
    #     'existing_weights': r'C:\Technion\Semester G\Project in Artificial Intelligence 236502\repo\approximate_q_learning_weights\res_1.pkl'}
    funds_df = pd.read_csv('funds_after_processing.csv').set_index('fund_symbol')
    funds_names = funds_df.index.unique().tolist()

    sim = Simulator(funds_csv=funds_df, funds_list_names=funds_names, investor=MonkeyInvestor)
    # Printer.print_funds(sim)
    # Printer.print_fund_symbols(sim)

    results_line = sim.run_simulator()
    print(results_line)
    # todo: change prints
    # todo: add rl q learning trainer
    # todo: make sure approx q learning works correctly after refactoring
    # Printer.print_results_path(results_line)
    # Printer.print_final_results(sim)
