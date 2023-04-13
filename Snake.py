import pygame
import random

class SnakeGame:

    def __init__(self, grid_cells_x = 20, grid_cells_y = 20) -> None:
        self.grid_cells_x = grid_cells_x
        self.grid_cells_y = grid_cells_y

        self.berry_pos = ()
        self.reset()       

    def reset(self):
        self.is_alive = True
        self.initial_pos = (self.grid_cells_x // 2, self.grid_cells_y // 2)
        self.snake = [self.initial_pos, (self.initial_pos[0], self.initial_pos[1] + 1)]

        self.max_queues = 3
        self.direction_queue = ["up"]
        self.directions = {"right": (1, 0), "down": (0, 1), "left": (-1, 0), "up": (0, -1)}

        self.set_berry_pos()

    def move(self):
        direction = self.direction_queue[0]
        if len(self.direction_queue) > 1:
            self.direction_queue.pop(0)

        new_x = self.snake[0][0] + self.directions[direction][0]
        new_y = self.snake[0][1] + self.directions[direction][1]
        self.snake.insert(0, (new_x, new_y))
        if self.snake[0] == self.berry_pos:
            self.set_berry_pos()
        else:
            self.snake.pop()
        if self.hit_body() or self.hit_wall():
            self.is_alive = False

    def add_to_direction_queue(self, direction):
        if len(self.direction_queue) < self.max_queues:
            self.direction_queue.append(direction)

    def set_berry_pos(self) -> None:
        self.berry_pos = (random.randint(0, self.grid_cells_x - 1), random.randint(0, self.grid_cells_y - 1))
        while self.berry_pos in self.snake:
            self.berry_pos = (random.randint(0, self.grid_cells_x - 1), random.randint(0, self.grid_cells_y - 1))
        
    def hit_body(self) -> None:
        return self.snake[0] in self.snake[1:]
    
    def hit_wall(self) -> None:
        hit_right = self.snake[0][0] > self.grid_cells_x - 1
        hit_bottom = self.snake[0][1] > self.grid_cells_y - 1
        hit_left = self.snake[0][0] < 0
        hit_top = self.snake[0][1] < 0
        return hit_right or hit_bottom or hit_left or hit_top


def draw_snake(body_part_positions):
    rect = pygame.Rect(body_part_positions[0][0] * grid_size_x, body_part_positions[0][1] * grid_size_y, grid_size_x, grid_size_y)
    pygame.draw.rect(screen, "Grey", rect)
    for body_part in body_part_positions[1:]:
        rect = pygame.Rect(body_part[0] * grid_size_x, body_part[1] * grid_size_y, grid_size_x, grid_size_y)
        pygame.draw.rect(screen, "Black", rect)


def draw_berry(berry_position):
    rect = pygame.Rect(berry_position[0] * grid_size_x, berry_position[1] * grid_size_y, grid_size_x, grid_size_y)
    pygame.draw.rect(screen, "Red", rect)


def new_game():
    snake.reset()
    screen.fill((255, 255, 255))
    draw_snake(snake.snake)
    pygame.display.update()


def game():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key in key_map.values():
            if event.key == key_map["right"] and not snake.direction_queue[-1] in ("right", "left"):
                snake.add_to_direction_queue("right")
            if event.key == key_map["down"] and not snake.direction_queue[-1] in ("down", "up"):
                snake.add_to_direction_queue("down")
            if event.key == key_map["left"] and not snake.direction_queue[-1] in ("right", "left"):
                snake.add_to_direction_queue("left")
            if event.key == key_map["up"] and not snake.direction_queue[-1] in ("down", "up"):
                snake.add_to_direction_queue("up")

        if event.type == pygame.QUIT:
            pygame.quit()

    snake.move()

    screen.fill((255, 255, 255))
    draw_snake(snake.snake)
    draw_berry(snake.berry_pos)
    pygame.display.update()

    clock.tick(FPS)


snake = SnakeGame(20, 20)
key_map = {"right": pygame.K_RIGHT,
           "down": pygame.K_DOWN,
           "left": pygame.K_LEFT,
           "up": pygame.K_UP,
           "start": pygame.K_SPACE}

pygame.init()
WIDTH = 600
HEIGHT = 600
FPS = 10
grid_size_x = WIDTH // snake.grid_cells_x
grid_size_y = HEIGHT // snake.grid_cells_y
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
run_game = False

screen.fill((255, 255, 255))
draw_snake(snake.snake)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key in key_map.values():
            if event.key == key_map["start"]:
                new_game()
                run_game = True
        if event.type == pygame.QUIT:
            pygame.quit()

    while run_game:
        game()
        if not snake.is_alive:
            run_game = False
    