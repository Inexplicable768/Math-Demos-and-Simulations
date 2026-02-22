# simple implementation of the game of life in python using pygame
# just made for fun

import pygame
import sys
import random

# Configuration
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# speed of the game (frames per second)
FPS = 10

# Colors
BG_COLOR = (10, 10, 10)
GRID_COLOR = (40, 40, 40)
ALIVE_COLOR = (0, 200, 0)
TEXT_COLOR = (200, 200, 200)

instructions = [
"SPACE: Start/Pause",
"C: Clear",
"R: Randomize",
"ESC: Quit",
"Press ENTER to hide this menu"
]
itter_count = 0
menu = True
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python - Conway's Game of Life")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)  # Create font once

def create_grid(randomize=False):
    if randomize:
        return [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

grid = create_grid()
running = False

def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, ALIVE_COLOR, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
def draw_stat():
    if menu:
        return
    alive_count = sum(sum(row) for row in grid)
    stat_text = f"Alive Cells: {alive_count} | Press SPACE to {'Pause' if running else 'Start'}"
    img = font.render(stat_text, True, TEXT_COLOR)
    screen.blit(img, (10, 20))
    # num of itterations
    itter_text = f"Iterations: {itter_count}"
    img2 = font.render(itter_text, True, TEXT_COLOR)
    screen.blit(img2, (10, 40))

def count_neighbors(x, y):
    total = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                total += grid[ny][nx]
    return total

def update_grid():
    global grid
    new_grid = create_grid()
    for y in range(ROWS):
        for x in range(COLS):
            neighbors = count_neighbors(x, y)
            if grid[y][x] == 1:
                if neighbors in (2, 3):
                    new_grid[y][x] = 1
            else:
                if neighbors == 3:
                    new_grid[y][x] = 1
    grid = new_grid

while True:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not running:
            mx, my = pygame.mouse.get_pos()
            x = mx // CELL_SIZE
            y = my // CELL_SIZE
            # Prevent edge crash
            if 0 <= x < COLS and 0 <= y < ROWS:
                grid[y][x] = 1 - grid[y][x]
            

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = not running
            elif event.key == pygame.K_c:
                grid = create_grid()
                running = False
            elif event.key == pygame.K_r:
                grid = create_grid(randomize=True)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:
                menu = False

    if running:
        update_grid()

    draw_grid()  # Always draw grid
    draw_stat()  # draw info

    if menu:
        for i, text in enumerate(instructions):
            img = font.render(text, True, TEXT_COLOR)
            screen.blit(img, (10, 10 + i * 20))

    if running:
        itter_count += 1
    pygame.display.flip()
    clock.tick(FPS)