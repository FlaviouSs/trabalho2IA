import numpy as np
from rl.qll_feature_extractor import FeatureExtractor

class Actions:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class CliffWalkingFeatureExtractor(FeatureExtractor):

    __actions_one_hot_encoding = {
        Actions.UP:         np.array([1, 0, 0, 0]), 
        Actions.RIGHT:      np.array([0, 1, 0, 0]),
        Actions.DOWN:       np.array([0, 0, 1, 0]),
        Actions.LEFT:       np.array([0, 0, 0, 1]),
    }

    def __init__(self, env):
        self.env = env
        self.features_list = [
            self.f_bias,
            self.f_column_progress,
            self.f_in_safe_corridor,
            self.f_cliff_fall,
            self.f_wall_bump,
            self.f_goal_drop,
        ]

    def get_num_features(self):
        return len(self.features_list) * self.get_num_actions()

    def get_num_actions(self):
        return len(self.get_actions())

    def get_actions(self):
        return [Actions.UP, Actions.RIGHT, Actions.DOWN, Actions.LEFT]

    def get_action_one_hot_encoded(self, action):
        return self.__actions_one_hot_encoding[action]

    def is_terminal_state(self, state):
        return state == 47

    def __future_position(self, state, action):
        row, col = divmod(int(state), 12)

        movements = {
            Actions.UP: (-1, 0),
            Actions.RIGHT: (0, 1),
            Actions.DOWN: (1, 0),
            Actions.LEFT: (0, -1)
        }

        dr, dc = movements[action]

        row = min(3, max(0, row + dr))
        col = min(11, max(0, col + dc))

        return row, col



    def get_features(self, state, action):
        state_features = np.array([
            feature(state, action)
            for feature in self.features_list
        ])

        action_vector = self.get_action_one_hot_encoded(action)

        return np.kron(state_features, action_vector)

    def f_bias(self, state, action):
        return 1.0

    def f_column_progress(self, state, action):
        row, col = divmod(state, 12)
        return col / 11.0

    def f_row_progress(self, state, action):
        row, col = divmod(state, 12)
        return row / 3.0

    def f_in_safe_corridor(self, state, action):
        row, col = divmod(state, 12)
        return 1.0 if row == 2 else 0.0

    def f_cliff_fall(self, state, action):
        row, col = divmod(state, 12)

        if action == Actions.RIGHT:
            return 1.0 if (row == 3 and col == 0) else 0.0

        if action == Actions.DOWN:
            return 1.0 if (row == 2 and 1 <= col <= 10) else 0.0

        return 0.0

    def f_wall_bump(self, state, action):
        row, col = divmod(state, 12)
        nr, nc = self.__future_position(state, action)
        return 1.0 if (nr == row and nc == col) else 0.0

    def f_goal_drop(self, state, action):
        row, col = divmod(state, 12)
        return 1.0 if (col == 11 and row < 3 and action == Actions.DOWN) else 0.0


    
"""
Comando de Treino:

i)  TABULAR

    python -m rl.ql_train --agent tabular --env_name CliffWalking-v1 --num_episodes 500 --learning_rate 0.1 --gamma 0.99 --epsilon_decay_rate 0.005 --plot

ii) LINEAR

    python -m rl.ql_train --agent linear --env_name CliffWalking-v1 --num_episodes 500 --learning_rate 0.02 --gamma 0.95 --epsilon_decay_rate 0.005 --plot

Comando para Jogar:

i)  TABULAR

    python -m rl.ql_play --agent tabular --env_name CliffWalking-v1 --num_episodes 5

ii) LINEAR

    python -m rl.ql_play --agent linear --env_name CliffWalking-v1 --num_episodes 5

"""