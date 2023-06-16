import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font(None, 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x , y")

BODY_SEGMENT_SIZE = 20
SPEED = 15
CATPPUCCIN_WHITE = (245, 224, 220)
CATPPUCCIN_RED = (210, 15, 57)
CATPPUCCIN_PINK = (234, 118, 203)
CATPPUCCIN_BLUE = (30, 102, 245)
CATPPUCCIN_BLUE_HL = (114, 135, 253)
CATPPUCCIN_BLACK = (17, 17, 27)
WINDOW_H = 480
WINDOW_W = 640

POSITIVE_REWARD = 10
NEGATIVE_REWARD = -10


class SnakeGameAI:
    def __init__(self):
        pygame.display.set_caption("SnakeAI")
        self.display = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.reset()

    def place_food(self):
        x = (
            random.randint(1, (WINDOW_W - BODY_SEGMENT_SIZE) // BODY_SEGMENT_SIZE)
            * BODY_SEGMENT_SIZE
        )
        y = (
            random.randint(1, (WINDOW_H - BODY_SEGMENT_SIZE) // BODY_SEGMENT_SIZE)
            * BODY_SEGMENT_SIZE
        )
        self.food = Point(x, y)
        if self.food in self.snake:
            self.place_food()

    def reset(self):
        self.food = None
        self.direction = Direction.RIGHT
        self.snake_head = Point(WINDOW_W / 2, WINDOW_H / 2)
        self.snake = [
            self.snake_head,
            Point(self.snake_head.x - BODY_SEGMENT_SIZE, self.snake_head.y),
            Point(self.snake_head.x - (2 * BODY_SEGMENT_SIZE), self.snake_head.y),
        ]
        self.score = 0
        self.frame_count = 0
        self.place_food()

    def move(self, action):
        # [Straight, right, left] one hotr encoded

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[index]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (index + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (index - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.snake_head.x
        y = self.snake_head.y
        if self.direction == Direction.RIGHT:
            x += BODY_SEGMENT_SIZE
        elif self.direction == Direction.LEFT:
            x -= BODY_SEGMENT_SIZE
        elif self.direction == Direction.DOWN:
            y += BODY_SEGMENT_SIZE
        elif self.direction == Direction.UP:
            y -= BODY_SEGMENT_SIZE
        self.snake_head = Point(x, y)

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.snake_head
        if (
            pt.x > WINDOW_W - BODY_SEGMENT_SIZE
            or pt.x < 0
            or pt.y > WINDOW_H - BODY_SEGMENT_SIZE
            or pt.y < 0
        ):
            return True
        if pt in self.snake[1:]:
            return True
        return False

    def game_tick(self):
        self.frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, self.score

        self.move()
        self.snake.insert(0, self.snake_head)
        reward = 0
        is_game_over = False
        if self.is_collision() or self.frame_count > 1000 * len(self.snake):
            is_game_over = True
            reward = NEGATIVE_REWARD
            return reward, is_game_over, self.score

        if self.snake_head == self.food:
            self.score += 1
            reward = POSITIVE_REWARD
            self.place_food()
        else:
            self.snake.pop()
        self.draw_frames()
        pygame.time.Clock().tick(SPEED)

        return reward, is_game_over, self.score

    def draw_frames(self):
        self.display.fill(CATPPUCCIN_BLACK)
        for pt in self.snake:
            pygame.draw.rect(
                self.display,
                CATPPUCCIN_BLUE,
                pygame.Rect(pt.x, pt.y, BODY_SEGMENT_SIZE, BODY_SEGMENT_SIZE),
            )
            pygame.draw.rect(
                self.display,
                CATPPUCCIN_BLUE_HL,
                pygame.Rect(pt.x + 4, pt.y + 4, 12, 12),
            )
        pygame.draw.rect(
            self.display,
            CATPPUCCIN_RED,
            pygame.Rect(self.food.x, self.food.y, BODY_SEGMENT_SIZE, BODY_SEGMENT_SIZE),
        )
        pygame.draw.rect(
            self.display,
            CATPPUCCIN_PINK,
            pygame.Rect(self.food.x + 4, self.food.y + 4, 12, 12),
        )
        text = font.render("Score: " + str(self.score), True, CATPPUCCIN_WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
