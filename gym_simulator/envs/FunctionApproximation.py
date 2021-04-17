import pathlib

import numpy as np
import pandas as pd
import random
import pickle
from numba import njit, jit

ACTIONS_NUMBER = 10
FEATURES_NUMBER = 6


@jit(nopython=True)
def fill_features(state_values, feaures_arr):
    # feature 0 is five years ago, feature 1 is 3 years ago, feature 2 is one year ago.
    # feature 5 to 8 is assets (stocks, bonds, cash, others)
    # features = np.ndarray([FEATURES_NUMBER, ACTIONS_NUMBER])
    feaures_arr[0, :] = state_values[:, 0] / 5 * 4
    feaures_arr[1, :] = state_values[:, 1] / 3 * 4
    feaures_arr[2, :] = state_values[:, 2] / 4
    feaures_arr[3, :] = state_values[:, 3]
    feaures_arr[4, :] = state_values[:, 4]

    def combined_assets_score(assets_relative_arr):
        return 0.8 * assets_relative_arr[0] + 0.15 * assets_relative_arr[1] + 0.05 * assets_relative_arr[2]

    for i in range(0, ACTIONS_NUMBER):
        fund_asset_score = combined_assets_score(state_values[i, 5:9])
        feaures_arr[5, i] = fund_asset_score
    return feaures_arr


class Estimator:
    def __init__(self, alpha=0.1, gamma=0.5, starting_weights=None, pickle_file_dir=None):
        if starting_weights is None:
            self._w = np.ones([FEATURES_NUMBER])
        else:
            self._w = starting_weights
        # self._w[1] = 2
        # self._w[2] = 3
        # self._w[3] = 5
        # self._w *= 100
        self._alpha = alpha
        self._gamma = gamma
        self._update_counter = 1
        if pickle_file_dir is None:
            self._file_dir = r'C:\Technion\Semester G\Project in Artificial Intelligence 236502\repo\approximate_q_learning_weights'
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
        features = fill_features(state_values, features)
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
        reward_standarize = reward * 100
        target = reward_standarize + self._gamma * self.get_state_max(next_state)
        prediction = self.get_q_value(state, action)
        delta_w = self._alpha * (target - prediction) * state_features
        self._w += delta_w

    def export_to_pickle(self, file_name):
        print(self._w)
        with open(pathlib.Path(self._file_dir) / file_name, "wb") as f:
            pickle.dump(self._w, f)
        print("Saved Successfully")
