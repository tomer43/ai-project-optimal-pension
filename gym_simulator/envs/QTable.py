import numpy as np
import random
import pickle


class QTable:
    def __init__(self, dictionary=None):
        if dictionary is None:
            dictionary = {}
        self._q_table = dictionary

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
        file = open("..\\..\\Q-Table.pkl", "wb")
        pickle.dump(self._q_table, file, protocol=4)
        file.close()
