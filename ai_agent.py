import torch
import random
import numpy as np
from collections import deque
from snake_game_ai import SnakeGameAI, Direction, Point, BODY_SEGMENT_SIZE
from model import Linear_QNet, QTrainer


MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.1  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

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
            game.food.x < game.snake_head.x,  # food left
            game.food.x > game.snake_head.x,  # food right
            game.food.y < game.snake_head.y,  # food up
            game.food.y > game.snake_head.y,  # food down
        ]

        return np.array(state, dtype=int)

    def game_memory(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_on_long_term_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_batch = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_batch = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_batch)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_on_short_term_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # explore phase
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


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
