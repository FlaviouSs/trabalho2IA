import numpy as np
from rl.qll_feature_extractor import FeatureExtractor

class Actions:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class CliffWalkingFeatureExtractor(FeatureExtractor):
    """
    Feature extractor for CliffWalking-v1 linear Q-learning.
    Extracts informative domain features based on the state-action transition.
    """
    ACTIONS_ONE_HOT = {
        Actions.UP:    np.array([1, 0, 0, 0]),
        Actions.RIGHT: np.array([0, 1, 0, 0]),
        Actions.DOWN:  np.array([0, 0, 1, 0]),
        Actions.LEFT:  np.array([0, 0, 0, 1]),
    }

    DELTA = {
        Actions.UP:    (-1, 0),
        Actions.RIGHT: (0, 1),
        Actions.DOWN:  (1, 0),
        Actions.LEFT:  (0, -1),
    }

    def __init__(self, env):
        self.env = env
        self.features_list = [
            self.f0_bias,
            self.f_is_goal,
            self.f_is_cliff,
            self.f_near_cliff,
            self.f_dist_goal,
            self.f_col_progress,
            self.f_row_height,
        ]

    def get_num_features(self):
        return len(self.features_list) + self.get_num_actions()

    def get_num_actions(self):
        return len(self.get_actions())

    def get_actions(self):
        return [Actions.UP, Actions.RIGHT, Actions.DOWN, Actions.LEFT]

    def get_action_one_hot_encoded(self, action):
        return self.ACTIONS_ONE_HOT[action]

    def is_terminal_state(self, state):
        return state == 47

    def _next_pos(self, state, action):
        r, c = state // 12, state % 12
        dr, dc = self.DELTA[action]
        nr = min(3, max(0, r + dr))
        nc = min(11, max(0, c + dc))
        return nr, nc

    def get_features(self, state, action):
        nr, nc = self._next_pos(state, action)
        feats = np.zeros(len(self.features_list), dtype=float)
        for i, fn in enumerate(self.features_list):
            feats[i] = fn(state, action, nr, nc)
        act_vec = self.get_action_one_hot_encoded(action)
        return np.concatenate([feats, act_vec])

    def f0_bias(self, state, action, nr, nc):
        return 1.0

    def f_is_goal(self, state, action, nr, nc):
        return 1.0 if (nr == 3 and nc == 11) else 0.0

    def f_is_cliff(self, state, action, nr, nc):
        return 1.0 if (nr == 3 and 1 <= nc <= 10) else 0.0

    def f_near_cliff(self, state, action, nr, nc):
        return 1.0 if (nr == 2 and 1 <= nc <= 10) else 0.0

    def f_dist_goal(self, state, action, nr, nc):
        manhattan = abs(nr - 3) + abs(nc - 11)
        return (14.0 - manhattan) / 14.0

    def f_col_progress(self, state, action, nr, nc):
        return nc / 11.0

    def f_row_height(self, state, action, nr, nc):
        return (3 - nr) / 3.0
