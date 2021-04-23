from gym_simulator.envs.QTable import QTable
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
import sys
from Config import *

import gym
import gym_simulator

from gym_simulator.envs.custom_env import CustomEnv

NUM_OF_ACTIONS = 10


def simulate():
    global epsilon, epsilon_decay
    episodes, sums = [], []
    for episode in range(MAX_EPISODES):

        # Init environment
        state = env.reset()
        total_reward = 0

        # AI tries up to MAX_TRY times
        for t in range(MAX_TRY):

            # In the beginning, do random action to learn
            if random.uniform(0, 1) < epsilon:
                # action = random.randint(0, 9)
                action = random.randint(0, NUM_OF_FUNDS - 1)
            else:
                action = q_table.get_state_argmax(state)

            # Do action and get result
            next_state, reward, done, _ = env.step(action)
            total_reward += reward

            # Get correspond q value from state, action pair
            q_value = q_table.get_q_value(state, action)

            best_q = q_table.get_state_max(next_state)

            # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
            q_table.update(state, action, learning_rate, q_value, reward, gamma, best_q)

            # Set up for the next iteration
            state = next_state

            # When episode is done, print reward
            if done or t >= MAX_TRY - 1:
                print("\nEpisode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                print()
                episodes.append(episode)
                sums.append(total_reward)
                break

        # exploring rate decay
        if epsilon >= 0.005:
            epsilon *= epsilon_decay

    q_table.export_to_pickle()
    print_episodes_results(sums)
        # i = 1
        # for y in y_values:
        #     print('{}: {}'.format(i, y))
        #     i += 1
    return episodes, sums


def print_episodes_results(sums):
    i = 1
    for s in sums:
        print(f'{i}: {s}')
        i += 1


def plot_unsmoothed_graph(episodes, sums):
    plt.xticks(episodes)
    plt.plot(episodes, sums)
    plt.show()


def plot_smoothed_graph(episodes, sums):
    df = pd.DataFrame({'Episode': episodes, 'Unsmoothed_sum': sums})
    df['Final Sum'] = df['Unsmoothed_sum'].rolling(MAX_EPISODES//100).mean()
    # df.plot.line(x='Episode', y=['Unsmoothed_sum', 'Final Sum'])
    df.plot.line(x='Episode', y='Final Sum')
    plt.show()


if __name__ == "__main__":
    # env = gym.make("Pysim-v0")
    env = CustomEnv()
    sys.stdout = open('main_results.txt', 'w')

    # MAX_EPISODES = 9999
    MAX_EPISODES = 250000
    MAX_TRY = 1000
    epsilon = 1
    epsilon_decay = 0.999
    learning_rate = 0.1
    gamma = 0.6
    q_table = QTable()
    episodes, sums = simulate()  # line semi-added by me: I added only left values

    # plotting RL algorithm learning curve
        # plt.xticks(x_values)
        # plt.plot(x_values, y_values)
        # plt.show()
    # plot_unsmoothed_graph(episodes, sums)
    plot_smoothed_graph(episodes, sums)


# if __name__ == "__main__":
#     # env = gym.make("Pysim-v0")
#     env = CustomEnv()
#
#     # MAX_EPISODES = 9999
#     MAX_EPISODES = 6000
#     MAX_TRY = 1000
#     epsilon = 1
#     epsilon_decay = 0.999
#     learning_rate = 0.1
#     gamma = 0.6
#     num_box = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
#     q_table = np.zeros(num_box + (env.action_space.n,))
#     x_values, y_values = simulate()     # line semi-added by me: I added only left values
#
#     # plotting RL algorithm learning curve
#     plt.xticks(x_values)                # line added by me
#     plt.plot(x_values, y_values)        # line added by me
#     plt.show()                          # line added by me


# -----------------------------------------------------------------------------------------------------------

# from gym_simulator.envs.QTable import QTable
# import sys
# import numpy as np
# import math
# import random
#
# import matplotlib.pyplot as plt
# import numpy as np
# import sys
#
# from numpy import asarray
# from numpy import savetxt
#
# import gym
# import gym_simulator
#
# from gym_simulator.envs.custom_env import CustomEnv
#
# NUM_OF_ACTIONS = 10
#
#
# def simulate():
#     global epsilon, epsilon_decay
#     x_values, y_values = [], []
#     for episode in range(MAX_EPISODES):
#
#         # Init environment
#         state = env.reset()
#         total_reward = 0
#
#         # AI tries up to MAX_TRY times
#         for t in range(MAX_TRY):
#
#             print('state = ', state)
#
#             # In the beginning, do random action to learn
#             if random.uniform(0, 1) < epsilon:
#                 # action = env.action_space.sample()
#                 action = random.randint(0, 9)
#             else:
#                     # if state in q_table:
#                     #     action = np.argmax(q_table[state])
#                     # else:
#                     #     action = random.randint(0, 9)       # if all q_values for this state are zeros
#                 action = q_table.get_state_argmax(state)
#
#
#             # print('action = ', action)          # line added by me
#
#             # Do action and get result
#             next_state, reward, done, _ = env.step(action)
#             total_reward += reward
#
#             # Get correspond q value from state, action pair
#                 # if state in q_table:
#                 #     q_value = q_table[state][action]
#                 # else:
#                 #     q_value = 0
#             q_value = q_table.get_q_value(state, action)
#
#
#             # print('next_state = ', next_state)       # line added by me
#                 # if next_state in q_table:
#                 #     best_q = np.max(q_table[next_state])
#                 # else:
#                 #     best_q = 0
#             best_q = q_table.get_state_max(next_state)
#
#             # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
#                 # if state not in q_table:
#                 #     q_table[state] = np.zeros(10)
#                 # q_table[state][action] = (1 - learning_rate) * q_value + learning_rate * (reward + gamma * best_q)
#             q_table.update(state, action, learning_rate, q_value, reward, gamma, best_q)
#
#             # Set up for the next iteration
#             state = next_state
#
#
#             # When episode is done, print reward
#             if done or t >= MAX_TRY - 1:
#                 print("\nEpisode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
#                 print()
#                 x_values.append(episode)
#                 y_values.append(total_reward)
#                 break
#
#         # exploring rate decay
#         if epsilon >= 0.005:
#             epsilon *= epsilon_decay
#
#     # savetxt('Q-Table.csv', q_table.get_q_table(), delimiter=',')
#
#     i = 1
#     for y in y_values:
#         print('{}: {}'.format(i, y))
#         i += 1
#     return x_values, y_values
