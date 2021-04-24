from gym.envs.registration import register

register(
    # id='Pygame-v0',
    id='Pysim-v0',
    entry_point='gym_simulator.envs:CustomEnv',
    max_episode_steps=2000,
)