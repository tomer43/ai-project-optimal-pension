import numpy as np
import pandas as pd
import random
import pickle

ACTIONS_NUMBER = 10
FEATURES_NUMBER = 5


class Estimator:
    def __init__(self, alpha=0.1, gamma=0.5):
        self._w = np.ones([FEATURES_NUMBER])
        self._w[1] = 2
        self._w[2] = 3
        self._w[3] = 5
        # self._w *= 100
        self._alpha = alpha
        self._gamma = gamma

    def get_weights(self):
        return self._w

    @staticmethod
    def featurize_state(state):
        features = state.values
        # features = np.ndarray([FEATURES_NUMBER, ACTIONS_NUMBER])
        # for i in range(FEATURES_NUMBER):
        #     for j in range(ACTIONS_NUMBER):
        #         features[i, j] = i*2
        return features

    def approximate_state(self, features, action_num):
        return features[:, action_num] @ self._w

    def get_estimated_q_vals(self, state, return_argmax):
        features_for_state = Estimator.featurize_state(state)
        vals = [self.approximate_state(features_for_state, action) for action in range(ACTIONS_NUMBER)]
        return np.argmax(vals) if return_argmax else np.max(vals)

    def get_state_max(self, state):
        return self.get_estimated_q_vals(state, return_argmax=False)

    def get_state_argmax(self, state):
        return self.get_estimated_q_vals(state, return_argmax=True)

    def get_q_value(self, state, action):
        return self.approximate_state(Estimator.featurize_state(state), action)

    def update(self, state, action, reward, state_prime):
        # return None
        state_features = self.featurize_state(state)[:, action]
        state_prime_features = self.featurize_state(state_prime)[:, self.get_state_argmax(state_prime)]
        reward_standarize = reward / 10000
        delta_w = self._alpha * (reward_standarize + self._gamma * state_prime_features.transpose() @ self._w - (
                    state_features.transpose() @ self._w)) * self._w
        self._w += delta_w
        self._w = self._w / np.sum(self._w)

    def export_to_pickle(self):
        raise NotImplementedError
        # file = open("E:\\Tomers Backup\\AI_project\\Q-Table.pkl", "wb")
        # file = open("Q-Table.pkl", "wb")
        # pickle.dump(self._q_table, file, protocol=4)
        # file.close()

        # df = pd.DataFrame.from_dict(self._q_table, orient='index', dtype=None, columns=None)
        # df.to_csv(r'QTABLE.csv')

        # import csv
        # csv_columns = ['features', 'fund_0', 'fund_1', 'fund_2', 'fund_3', 'fund_4', 'fund_5', 'fund_6', 'fund_7', 'fund_8', 'fund_9']
        # dict_data = self._q_table
        # csv_file = "Q_TABLE.csv"
        # try:
        #     with open(csv_file, 'w') as csvfile:
        #         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        #         writer.writeheader()
        #         for data in dict_data:
        #             writer.writerow(dict_data)
        # except IOError:
        #     print("I/O error")