import random
from tqdm import tqdm
import sys
import pickle
import pathlib

import pandas as pd
import matplotlib.pyplot as plt

from gym_simulator.envs.custom_env import CustomEnv
from gym_simulator.envs.FunctionApproximation import Estimator


from investors_types.RLInvestor import RLApproximateQInvestor


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


class TrainerApproximateRL:
    def __init__(self, funds_csv, funds_names_list, max_episodes, max_try=1000, learning_constant=10,
                 gamma=0.6, weights_to_start_dir=None):
        rl_kwargs = {}
        estimator_args = {
            "alpha": 1 / learning_constant,
            "gamma": gamma,
            "pickle_file_dir": pathlib.Path("../../approximate_q_learning_weights"),
        }
        if weights_to_start_dir is not None:
            rl_kwargs['existing_weights'] = weights_to_start_dir
        rl_kwargs['estimator_kwargs'] = estimator_args

        self._env = CustomEnv(funds_csv=funds_csv, funds_names=funds_names_list, investor=RLApproximateQInvestor,
                              investor_kwargs=rl_kwargs)
        self._max_episodes = max_episodes
        self._max_try = max_try

        self._estimator = self._env.get_investor().get_inner_estimator()
        # if weights_to_start_dir is None:
        #     trainer_starting_weights=None
        # else:
        #     with open(weights_to_start_dir, 'rb') as f:
        #         trainer_starting_weights = pickle.load(f)
        #
        # self._estimator = Estimator(alpha=1 / learning_constant, gamma=gamma, starting_weights=trainer_starting_weights,
        #                             pickle_file_dir=r'C:\Technion\Semester G\Project in Artificial Intelligence 236502\repo\approximate_q_learning_weights')

    def train(self):
        # global epsilon, epsilon_decay
        # sys.stdout = open('training_results.txt', 'w')
        episodes, sums = [], []

        for episode in tqdm(range(self._max_episodes), desc="\tProgress"):

            # Init environment
            state = self._env.reset()
            total_reward = 100000

            # AI tries up to MAX_TRY times
            for t in range(self._max_try):

                # In the beginning, do random action to learn
                action = self._estimator.get_state_argmax(state)

                # Do action and get result
                next_state, reward, done, _ = self._env.step(action)
                relative_reward = reward / total_reward if total_reward > 0 else reward
                total_reward += reward

                # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
                self._estimator.update(state=state, action=action, reward=relative_reward, next_state=next_state)

                # Set up for the next iteration
                state = next_state

                # When episode is done
                if done or t >= self._max_try - 1:
                    # once in 50,000 episodes: print some stats and save to pickle
                    if episode % 50000 == 0:
                        self._estimator.export_to_pickle(f'agent_v1_e{episode}.pkl')
                        print("\nEpisode %d finished after %i time steps with total reward = %f." % (episode, t,
                                                                                                     total_reward))
                        print(f'weights: {self._estimator.get_weights()}')
                        print()

                    episodes.append(episode)
                    sums.append(total_reward)
                    break

        self._estimator.export_to_pickle('final_weights.pkl')
        print_episodes_results(sums)

        # plotting RL algorithm learning curve
        plot_smoothed_graph(episodes, sums, self._max_episodes)
        # return self._q_table
        return None


if __name__ == '__main__':
    funds_df = pd.read_csv('../../funds_after_processing.csv').set_index('fund_symbol')
    funds_names = funds_df.index.unique().tolist()

    # starting_weights = pathlib.Path('../../approximate_q_learning_weights/agent_debugging_mid.pkl')
    starting_weights = None
    
    trainer = TrainerApproximateRL(funds_csv=funds_df, funds_names_list=funds_names, max_episodes=60000,
                                   learning_constant=100000, gamma=0, weights_to_start_dir=starting_weights)
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
