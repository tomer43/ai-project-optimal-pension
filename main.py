import sys
import numpy as np
import math
import random

import matplotlib.pyplot as plt
import numpy as np

import gym
import gym_simulator

from gym_simulator.envs.custom_env import CustomEnv

def simulate():
    global epsilon, epsilon_decay
    x_values = []       # line added by me
    y_values = []       # line added by me
    for episode in range(MAX_EPISODES):

        # Init environment
        state = env.reset()
        total_reward = 0

        # AI tries up to MAX_TRY times
        for t in range(MAX_TRY):

            # In the beginning, do random action to learn
            if random.uniform(0, 1) < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[state])

            print('action = ', action)          # line added by me

            # Do action and get result
            next_state, reward, done, _ = env.step(action)
            total_reward += reward

            # Get correspond q value from state, action pair
            q_value = q_table[state][action]
            print('next_state = ', next_state)       # line added by me
            best_q = np.max(q_table[next_state])

            # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
            q_table[state][action] = (1 - learning_rate) * q_value + learning_rate * (reward + gamma * best_q)

            # Set up for the next iteration
            state = next_state

            # Draw games
            env.render()

            # When episode is done, print reward
            if done or t >= MAX_TRY - 1:
                print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                x_values.append(episode)            # line added by me
                y_values.append(total_reward)       # line added by me
                break

        # exploring rate decay
        if epsilon >= 0.005:
            epsilon *= epsilon_decay

    # print('final money:\t', y_values)
    for y in y_values:
        print(y)
    return x_values, y_values


if __name__ == "__main__":
    # env = gym.make("Pysim-v0")
    env = CustomEnv()

    # MAX_EPISODES = 9999
    MAX_EPISODES = 7000
    MAX_TRY = 1000
    epsilon = 1
    epsilon_decay = 0.999
    learning_rate = 0.1
    gamma = 0.6
    num_box = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
    q_table = np.zeros(num_box + (env.action_space.n,))
    x_values, y_values = simulate()     # line semi-added by me: I added only left values

    # plotting RL algorithm learning curve
    plt.xticks(x_values)                # line added by me
    plt.plot(x_values, y_values)        # line added by me
    plt.show()                          # line added by me




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
