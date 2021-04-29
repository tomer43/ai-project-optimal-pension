from investors_types.HumanHeuristicsInvestors import *
from RL_Trainer.FunctionApproximation import Estimator


class RLQInvestor(Investor):
    def __init__(self, initial_money, **kwargs):
        super().__init__(initial_money)
        if 'q_table' not in kwargs.keys():
            raise ValueError("Missing Q table! Run TrainerRL.TrainerQLearning.train() first")
        self._q_table = kwargs['q_table']

    def choose_fund(self, state):
        hashed_state = state.tobytes().__hash__()
        action = self._q_table.get_state_argmax(hashed_state)
        return action


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
