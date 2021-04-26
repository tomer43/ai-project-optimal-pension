import numpy as np
from gym_simulator.envs.State import State
import pickle
from gym_simulator.envs.QTable import QTable
from numpy import loadtxt
from investors_types.HumanHeuristicsInvestors import *
from gym_simulator.envs.FunctionApproximation import Estimator


# class RLInvestor(Investor):
#     def __init__(self, initial_money, existing_weights=None):
#         super().__init__(initial_money)
#         if existing_weights is None:
#             self._estimator = TrainerApproximateRL(max_episodes=100).train()
#         else:
#             self._estimator = Estimator()
#             self._estimator.load_existing_weights(file_dir=existing_weights)
#
#     def choose_fund(self, funds, quarter):      # TODO: check if the order of the actions in tthe Qtable matches the order of the funds in self._funds
#         state = State(funds, quarter).get_state()
#         action = self._estimator.get_state_argmax(state)
#         next_fund = funds[action]
#         return next_fund


class RLApproximateQInvestor(Investor):
    def __init__(self, initial_money, existing_weights=None, estimator_kwargs=None):
        super().__init__(initial_money)
        if estimator_kwargs is not None:
            self._estimator = Estimator(**estimator_kwargs)
        else:
            self._estimator = Estimator()
        if existing_weights is not None:
            self._estimator.load_existing_weights(file_dir=existing_weights)

    def choose_fund(self, state):
        action = self._estimator.get_state_argmax(state)
        return action

    def get_inner_estimator(self):
        return self._estimator


# ---------------------------------------------------------------------------------
class RLQInvestor(Investor):
    def __init__(self, initial_money, **kwargs):
        super().__init__(initial_money)
        # if q_table is None:
            # self._q_table = QTable(pickle.load(open(kwargs['q_table'], "rb")))
        if 'q_table' not in kwargs.keys():
            raise ValueError("Missing Q table")
        self._q_table = kwargs['q_table']
        # else:
        #     self._q_table = q_table
        # self._q_table = TrainerRL(max_episodes=100).train() # Final result too big- check how many random choices were there
        # self._q_table = QTable(pickle.load(open("Q-Table.pkl", "rb")))

    def choose_fund(self, state):      # TODO: check if the order of the actions in tthe Qtable matches the order of the funds in self._funds
        hashed_state = state.tobytes().__hash__()
        action = self._q_table.get_state_argmax(hashed_state)
        # # print(f'RLInvestor action: {action}')
        # next_fund = funds[action]
        return action
# ---------------------------------------------------------------------------------

# Before changing to features as states
# import numpy as np
# from numpy import loadtxt
# from investors_types.Investor import Investor
# from investors_types.HumanHeuristicsInvestors import *
#
# actions = [BestReturnLastQuarterInvestor, BestReturnLastYearInvestor, BestReturnLastThreeYearsInvestor,
#            BestReturnLastFiveYearsInvestor, TechnologyInvestor, RealEstateInvestor,
#            LargestFundInvestor, ExpertAdviceInvestor, LowestFeeInvestor]
#
# class RLInvestor(Investor):
#     def __init__(self, initial_money):
#         super().__init__(initial_money)
#         self._q_table = loadtxt('Q-Table.csv', delimiter=',')
#
#     def choose_fund(self, funds, quarter):
#         action = np.argmax(self._q_table[int(self._current_money)])
#         # print(f'RLInvestor action: {action}')
#         investor_type = actions[action]
#         temp_investor = investor_type(self._current_money)
#         next_fund = temp_investor.choose_fund(funds, quarter)
#         del temp_investor
#         return next_fund