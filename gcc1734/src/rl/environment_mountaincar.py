from rl.environment import Environment
import numpy as np

class MountainCarEnvironment(Environment):
    def __init__(self, env, bins=30):
        super().__init__(env)
        self.bins = bins

        self.pos_bins = np.linspace(self.env.observation_space.low[0], self.env.observation_space.high[0], bins)
        self.vel_bins = np.linspace(self.env.observation_space.low[1], self.env.observation_space.high[1], bins)

    def get_num_states(self):
        return self.bins * self.bins

    def get_num_actions(self):
        return self.env.action_space.n

    def get_state_id(self, state):
        
        pos, vel = state

        # returns bin index (subtract 1 for 0-based indexing)
        pos_idx = np.digitize(pos, self.pos_bins) - 1
        vel_idx = np.digitize(vel, self.vel_bins) - 1

        # Clamp indices [0, bins - 1]
        pos_idx = min(self.bins - 1, max(0, pos_idx))
        vel_idx = min(self.bins - 1, max(0, vel_idx))

        # Flatten 2D grid index (pos_idx, vel_idx) into a unique scalar state ID
        return pos_idx * self.bins + vel_idx

    def get_random_action(self):
        return self.env.action_space.sample()