import pathlib

import numpy as np
import pickle
from numba import jit

from gym_simulator.envs.State import get_state_features_to_idx

ACTIONS_NUMBER = 10
FEATURES_NUMBER = 6
FEATURES_IDX = get_state_features_to_idx()


@jit(nopython=True)
def fill_features(state_values, features_arr, returns_idx_start, expense_ratio_idx, assets_start_idx):
    # feature 0 is five years ago, feature 1 is 3 years ago, feature 2 is one year ago.
    # feature 5 to 8 is assets (stocks, bonds, cash, others)
    features_arr[0, :] = state_values[:, returns_idx_start] / 5 * 4
    features_arr[1, :] = state_values[:, returns_idx_start + 1] / 3 * 4
    features_arr[2, :] = state_values[:, returns_idx_start + 2] / 4
    features_arr[3, :] = state_values[:, returns_idx_start + 3]
    features_arr[4, :] = state_values[:, expense_ratio_idx]

    def combined_assets_score(assets_relative_arr):
        return 0.8 * assets_relative_arr[0] + 0.15 * assets_relative_arr[1] + 0.05 * assets_relative_arr[2]

    assets_idx_st = assets_start_idx
    assets_idx_end = assets_start_idx + 4
    for i in range(0, ACTIONS_NUMBER):
        fund_asset_score = combined_assets_score(state_values[i, assets_idx_st:assets_idx_end])
        features_arr[5, i] = fund_asset_score
    return features_arr


class Estimator:
    def __init__(self, alpha=0.1, gamma=0.5, starting_weights=None, pickle_file_dir=None):
        if starting_weights is None:
            self._w = np.ones([FEATURES_NUMBER])
        else:
            self._w = starting_weights
        self._alpha = alpha
        self._gamma = gamma
        self._update_counter = 1
        if pickle_file_dir is None:
            self._file_dir = pathlib.Path('../../approximate_q_learning_weights/')
        else:
            self._file_dir = pickle_file_dir

    def get_weights(self):
        return self._w

    def load_existing_weights(self, file_dir):
        with open(file_dir, 'rb') as f:
            self._w = pickle.load(f)

    @staticmethod
    def featurize_state(state_values):
        features = np.zeros(shape=[FEATURES_NUMBER, ACTIONS_NUMBER])
        return_idx = FEATURES_IDX['fund_total_last_5_years_returns']
        expense_ratio_idx = FEATURES_IDX['fund_quarterly_expense_ratio']
        assets_idx = FEATURES_IDX['asset_stocks']

        features = fill_features(state_values=state_values, features_arr=features, returns_idx_start=return_idx,
                                 expense_ratio_idx=expense_ratio_idx, assets_start_idx=assets_idx)
        return features

    def approximate_state(self, features, action_num):
        return np.dot(features[:, action_num], self._w)

    def get_estimated_q_vals(self, state, return_argmax):
        features_for_state = Estimator.featurize_state(state)
        vals = np.zeros(shape=[ACTIONS_NUMBER, ])
        for action in range(ACTIONS_NUMBER):
            vals[action] = self.approximate_state(features_for_state, action)
        return np.argmax(vals) if return_argmax else np.max(vals)

    def get_state_max(self, state):
        return self.get_estimated_q_vals(state, return_argmax=False)

    def get_state_argmax(self, state):
        return self.get_estimated_q_vals(state, return_argmax=True)

    def get_q_value(self, state, action):
        return self.approximate_state(Estimator.featurize_state(state), action)

    def update(self, state, action, reward, next_state):
        state_features = self.featurize_state(state)[:, action]
        reward_standardized = reward * 100
        target = reward_standardized + self._gamma * self.get_state_max(next_state)
        prediction = self.get_q_value(state, action)
        delta_w = self._alpha * (target - prediction) * state_features
        self._w += delta_w

    def export_to_pickle(self, file_name):
        print(self._w)
        with open(pathlib.Path(self._file_dir) / file_name, "wb") as f:
            pickle.dump(self._w, f)
        print("Saved Successfully")
