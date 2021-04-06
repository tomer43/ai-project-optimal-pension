from gym_simulator.envs.QTable import QTable
from gym_simulator.envs.custom_env import CustomEnv
import pandas as pd
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
import sys


def print_episodes_results(sums):
    i = 1
    for s in sums:
        print(f'{i}: {s}')
        i += 1


def plot_unsmoothed_graph(episodes, sums):
    plt.xticks(episodes)
    plt.plot(episodes, sums)
    plt.show()


def plot_smoothed_graph(episodes, sums, max_episodes):
    df = pd.DataFrame({'Episode': episodes, 'Unsmoothed_sum': sums})
    df['Final Sum'] = df['Unsmoothed_sum'].rolling(max_episodes // 100).mean()
    # df.plot.line(x='Episode', y=['Unsmoothed_sum', 'Final Sum'])
    df.plot.line(x='Episode', y='Final Sum')
    plt.show()


class TrainerRL:
    def __init__(self, max_episodes, max_try=1000, epsilon=1, epsilon_decay=0.999, learning_rate=0.1,
                 gamma=0.6, q_table=None):
        self._env = CustomEnv()
        self._max_episodes = max_episodes
        self._max_try = max_try
        self._epsilon = epsilon
        self._epsilon_decay = epsilon_decay
        self._learning_rate = learning_rate
        self._gamma = gamma
        if q_table is None:
            self._q_table = QTable()
        else:
            self._q_table = q_table

    def train(self):
        # global epsilon, epsilon_decay
        sys.stdout = open('training_results.txt', 'w')
        episodes, sums = [], []

        for episode in tqdm(range(self._max_episodes), desc="\tProgress"):
        # for episode in range(self._max_episodes):

            # Init environment
            state = self._env.reset()
            total_reward = 0

            # AI tries up to MAX_TRY times
            for t in range(self._max_try):

                # In the beginning, do random action to learn
                if random.uniform(0, 1) < self._epsilon:
                    action = random.randint(0, 9)
                else:
                    action = self._q_table.get_state_argmax(state)

                # Do action and get result
                next_state, reward, done, _ = self._env.step(action)
                total_reward += reward

                # Get correspond q value from state, action pair
                q_value = self._q_table.get_q_value(state, action)

                best_q = self._q_table.get_state_max(next_state)

                # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
                self._q_table.update(state, action, self._learning_rate, q_value, reward, self._gamma, best_q)

                # Set up for the next iteration
                state = next_state

                # When episode is done, print reward
                if done or t >= self._max_try - 1:
                    print("\nEpisode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                    print()
                    episodes.append(episode)
                    sums.append(total_reward)
                    break

            # exploring rate decay
            if self._epsilon >= 0.005:
                self._epsilon *= self._epsilon_decay

        self._q_table.export_to_pickle()
        print_episodes_results(sums)

        # plotting RL algorithm learning curve
        plot_smoothed_graph(episodes, sums, self._max_episodes)
        return self._q_table

if __name__ == '__main__':
    trainer = TrainerRL(max_episodes=100)
    trainer.train()

# # env = gym.make("Pysim-v0")
#     env = CustomEnv()
#     sys.stdout = open('main_results.txt', 'w')
#
#     # MAX_EPISODES = 9999
#     MAX_EPISODES = 250000
#     MAX_TRY = 1000
#     epsilon = 1
#     epsilon_decay = 0.999
#     learning_rate = 0.1
#     gamma = 0.6
#     q_table = QTable()
#     episodes, sums = simulate()  # line semi-added by me: I added only left values
#
#     # plotting RL algorithm learning curve
#     # plot_unsmoothed_graph(episodes, sums)
#     plot_smoothed_graph(episodes, sums)
