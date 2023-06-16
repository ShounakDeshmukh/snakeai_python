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


# im using global variables sue me
display = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("SnakeAI")

direction = Direction.RIGHT
snake_head = Point(WINDOW_W / 2, WINDOW_H / 2)
snake = [
    snake_head,
    Point(snake_head.x - BODY_SEGMENT_SIZE, snake_head.y),
    Point(snake_head.x - (2 * BODY_SEGMENT_SIZE), snake_head.y),
]
score = 0


def place_food():
    global food, snake
    x = (
        random.randint(1, (WINDOW_W - BODY_SEGMENT_SIZE) // BODY_SEGMENT_SIZE)
        * BODY_SEGMENT_SIZE
    )
    y = (
        random.randint(1, (WINDOW_H - BODY_SEGMENT_SIZE) // BODY_SEGMENT_SIZE)
        * BODY_SEGMENT_SIZE
    )
    food = Point(x, y)
    if food in snake:
        place_food()


def move():
    global snake_head
    x = snake_head.x
    y = snake_head.y
    if direction == Direction.RIGHT:
        x += BODY_SEGMENT_SIZE
    elif direction == Direction.LEFT:
        x -= BODY_SEGMENT_SIZE
    elif direction == Direction.DOWN:
        y += BODY_SEGMENT_SIZE
    elif direction == Direction.UP:
        y -= BODY_SEGMENT_SIZE
    snake_head = Point(x, y)


def is_collision():
    global snake, snake_head, WINDOW_W, WINDOW_H
    if (
        snake_head.x > WINDOW_W - BODY_SEGMENT_SIZE
        or snake_head.x < 0
        or snake_head.y > WINDOW_H - BODY_SEGMENT_SIZE
        or snake_head.y < 0
    ):
        return True
    if snake_head in snake[1:]:
        return True
    return False


def game_tick():
    global direction, snake_head, snake, score, food
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, score
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != Direction.RIGHT:
                direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT and direction != Direction.LEFT:
                direction = Direction.RIGHT
            elif event.key == pygame.K_UP and direction != Direction.DOWN:
                direction = Direction.UP
            elif event.key == pygame.K_DOWN and direction != Direction.UP:
                direction = Direction.DOWN

    move()
    snake.insert(0, snake_head)

    isgame_over = False
    if is_collision():
        isgame_over = True
    if snake_head == food:
        score += 1
        place_food()
    else:
        snake.pop()
    if is_collision():
        isgame_over = True
    draw_frames()
    pygame.time.Clock().tick(SPEED)

    return isgame_over, score


def draw_frames():
    global display, snake, food, score
    display.fill(CATPPUCCIN_BLACK)
    for pt in snake:
        pygame.draw.rect(
            display,
            CATPPUCCIN_BLUE,
            pygame.Rect(pt.x, pt.y, BODY_SEGMENT_SIZE, BODY_SEGMENT_SIZE),
        )
        pygame.draw.rect(
            display, CATPPUCCIN_BLUE_HL, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12)
        )
    pygame.draw.rect(
        display,
        CATPPUCCIN_RED,
        pygame.Rect(food.x, food.y, BODY_SEGMENT_SIZE, BODY_SEGMENT_SIZE),
    )
    pygame.draw.rect(
        display,
        CATPPUCCIN_PINK,
        pygame.Rect(food.x + 4, food.y + 4, 12, 12),
    )
    text = font.render("Score: " + str(score), True, CATPPUCCIN_WHITE)
    display.blit(text, [0, 0])
    pygame.display.flip()


def main():
    place_food()
    game_over = False
    while not game_over:
        game_over, score = game_tick()

    print("Final Score:", score)
    pygame.quit()


if __name__ == "__main__":
    main()
