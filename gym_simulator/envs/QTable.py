import numpy as np
import pandas as pd
import random
import pickle

class QTable:
    def __init__(self, dict=None):
        if dict is None:
            dict = {}
        self._q_table = dict

    def get_q_table(self):
        return self._q_table

    def get_state_max(self, state):
        if state in self._q_table:
            best_q = np.max(self._q_table[state])
        else:
            best_q = 0
        return best_q

    def get_state_argmax(self, state):
        if state in self._q_table:
            action = np.argmax(self._q_table[state])
        else:
            action = random.randint(0, 9)  # if all q_values for this state are zeros
        return action

    def get_q_value(self, state, action):
        if state in self._q_table:
            q_value = self._q_table[state][action]
        else:
            q_value = 0
        return q_value

    def update(self, state, action, learning_rate, q_value, reward, gamma, best_q):
        if state not in self._q_table:
            self._q_table[state] = np.zeros(10)
        self._q_table[state][action] = (1 - learning_rate) * q_value + learning_rate * (reward + gamma * best_q)

    def export_to_pickle(self):
        # file = open("E:\\Tomers Backup\\AI_project\\Q-Table.pkl", "wb")
        file = open("Q-Table.pkl", "wb")
        pickle.dump(self._q_table, file, protocol=4)
        file.close()

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