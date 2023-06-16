import pygame
import random
from enum import Enum
from collections import namedtuple

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


class SnakeGameAI:
    def __init__(self):
        pygame.display.set_caption("SnakeAI")
        self.display = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.reset()
        self.frame_count = 0

        self.place_food()

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
        self.direction = Direction.RIGHT
        self.snake_head = Point(WINDOW_W / 2, WINDOW_H / 2)
        self.snake = [
            self.snake_head,
            Point(self.snake_head.x - BODY_SEGMENT_SIZE, self.snake_head.y),
            Point(self.snake_head.x - (2 * BODY_SEGMENT_SIZE), self.snake_head.y),
        ]
        self.score = 0

    def move(self):
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

    def is_collision(self):
        if (
            self.snake_head.x > WINDOW_W - BODY_SEGMENT_SIZE
            or self.snake_head.x < 0
            or self.snake_head.y > WINDOW_H - BODY_SEGMENT_SIZE
            or self.snake_head.y < 0
        ):
            return True
        if self.snake_head in self.snake[1:]:
            return True
        return False

    def game_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, self.score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        self.move()
        self.snake.insert(0, self.snake_head)

        is_game_over = False
        if self.is_collision():
            is_game_over = True
        if self.snake_head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()
        if self.is_collision():
            is_game_over = True
        self.draw_frames()
        pygame.time.Clock().tick(SPEED)

        return is_game_over, self.score

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


if __name__ == "__main__":
    snake_game = SnakeGameAI()
    is_game_over = False
    while not is_game_over:
        is_game_over, score = snake_game.game_tick()
    print("Final Score:", score)
    pygame.quit()
