import numpy as np
from rl.qll_feature_extractor import FeatureExtractor

class Actions:
    LEFT = 0
    DOWN = 1
    RIGHT = 2
    UP = 3

class FrozenLakeFeatureExtractor(FeatureExtractor):
    """
    Feature extractor for FrozenLake-v1 linear Q-learning.
    Extracts geometric and hazard-aware features for the 4x4 slippery lake.
    """
    ACTIONS_ONE_HOT = {
        Actions.LEFT:  np.array([1, 0, 0, 0]),
        Actions.DOWN:  np.array([0, 1, 0, 0]),
        Actions.RIGHT: np.array([0, 0, 1, 0]),
        Actions.UP:    np.array([0, 0, 0, 1]),
    }

    DELTA = {
        Actions.LEFT:  (0, -1),
        Actions.DOWN:  (1, 0),
        Actions.RIGHT: (0, 1),
        Actions.UP:    (-1, 0),
    }

    HOLES = {(1, 1), (1, 3), (2, 3), (3, 0)}

    def __init__(self, env):
        self.env = env
        self.features_list = [
            self.f0_bias,
            self.f_is_goal,
            self.f_is_hole,
            self.f_dist_goal,
            self.f_dist_nearest_hole,
            self.f_progress,
        ]

    def get_num_features(self):
        return len(self.features_list) + self.get_num_actions()

    def get_num_actions(self):
        return 4

    def get_actions(self):
        return [Actions.LEFT, Actions.DOWN, Actions.RIGHT, Actions.UP]

    def get_action_one_hot_encoded(self, action):
        return self.ACTIONS_ONE_HOT[action]

    def is_terminal_state(self, state):
        r, c = state // 4, state % 4
        return (r, c) == (3, 3) or (r, c) in self.HOLES

    def _intended_next_pos(self, state, action):
        r, c = state // 4, state % 4
        dr, dc = self.DELTA[action]
        nr = min(3, max(0, r + dr))
        nc = min(3, max(0, c + dc))
        return nr, nc

    def get_features(self, state, action):
        nr, nc = self._intended_next_pos(state, action)
        feats = np.zeros(len(self.features_list), dtype=float)
        for i, fn in enumerate(self.features_list):
            feats[i] = fn(state, action, nr, nc)
        act_vec = self.get_action_one_hot_encoded(action)
        return np.concatenate([feats, act_vec])

    def f0_bias(self, state, action, nr, nc):
        return 1.0

    def f_is_goal(self, state, action, nr, nc):
        return 1.0 if (nr == 3 and nc == 3) else 0.0

    def f_is_hole(self, state, action, nr, nc):
        return 1.0 if (nr, nc) in self.HOLES else 0.0

    def f_dist_goal(self, state, action, nr, nc):
        manhattan = abs(nr - 3) + abs(nc - 3)
        return (6.0 - manhattan) / 6.0

    def f_dist_nearest_hole(self, state, action, nr, nc):
        min_dist = min(abs(nr - hr) + abs(nc - hc) for hr, hc in self.HOLES)
        return min_dist / 6.0

    def f_progress(self, state, action, nr, nc):
        return (nr + nc) / 6.0
