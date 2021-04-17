import gym
from gym import spaces
import pandas as pd
import numpy as np
from investors_types.HumanHeuristicsInvestors import *
# from gym_simulator.envs.pygame_2d import PyGame2D
from gym_simulator.envs.SimulatorRL import SimulatorRL


NUM_OF_HUMAN_HEURISTICS = 6
INITIAL_MONEY = 100000
funds_csv = pd.read_csv(r'C:\Technion\Semester G\Project in Artificial Intelligence 236502\repo/funds_after_processing.csv').set_index('fund_symbol')
# funds_names = funds_csv['fund_symbol'].unique().tolist()
funds_names = funds_csv.index.unique().tolist()
DEBUG_MODE = False


class CustomEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        # self.pygame = PyGame2D()
        # funds_csv = pd.read_csv('funds_after_processing.csv')
        self.pygame = SimulatorRL(funds_csv, initial_money=INITIAL_MONEY, investor=Investor, debug_mode=DEBUG_MODE,
                                  funds_names=funds_names)
        # self.action_space = spaces.Discrete(10)     # action is choosing a fund
        # self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), high=np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]), dtype=np.float32)

    def reset(self):
        del self.pygame
        self.pygame = SimulatorRL(funds_csv, initial_money=INITIAL_MONEY, investor=Investor, debug_mode=DEBUG_MODE,
                                  funds_names=funds_names)
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}
