import numpy as np
import tensorflow as tf
from tensorflow import keras
import random
from snake_game_ai import SnakeGameAI, Point, Direction, BODY_SEGMENT_SIZE
from collections import deque


MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = None
        self.trainer = None
        # TODO: model and tainer

    def get_state(self, game):
        head = game.snake[0]
        point_left = Point(head.x - BODY_SEGMENT_SIZE, head.y)
        point_right = Point(head.x + BODY_SEGMENT_SIZE, head.y)
        point_up = Point(head.x, head.y - BODY_SEGMENT_SIZE)
        point_down = Point(head.x, head.y + BODY_SEGMENT_SIZE)

        dir_left = game.direction == Direction.LEFT
        dir_right = game.direction == Direction.RIGHT
        dir_up = game.direction == Direction.UP
        dir_down = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_right and game.is_collision(point_right))
            or (dir_left and game.is_collision(point_left))
            or (dir_up and game.is_collision(point_up))
            or (dir_down and game.is_collision(point_down)),
            # Danger right
            (dir_up and game.is_collision(point_right))
            or (dir_down and game.is_collision(point_left))
            or (dir_left and game.is_collision(point_up))
            or (dir_right and game.is_collision(point_down)),
            # Danger left
            (dir_down and game.is_collision(point_right))
            or (dir_up and game.is_collision(point_left))
            or (dir_right and game.is_collision(point_up))
            or (dir_left and game.is_collision(point_down)),
            dir_left,
            dir_right,
            dir_up,
            dir_down,
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y,  # food down
        ]

        return np.array(state, dtype=int)

    def game_memory(self, state, action, reward, next_state, done):
        self.memory.append(state, action, reward, next_state, done)

    def train_on_long_term_memory(self):
        pass

    def train_on_short_term_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass


def train():
    scores = []
    mean_scores = []
    total_score = 0
    high_score = 0
    agent = Agent()
    game = SnakeGameAI()

    while True:
        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        reward, done, score = game.game_tick(final_move)

        state_new = agent.get_state(game)

        agent.train_on_short_term_memory(state_old, final_move, reward, state_new, done)

        agent.game_memory(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_on_long_term_memory()
            if score > high_score:
                high_score = score
                # save model
            print("Game", agent.n_games, "Score", score, "Record:", high_score)


if __name__ == "__main__":
    train()
