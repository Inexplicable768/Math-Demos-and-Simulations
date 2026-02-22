# chaos game (n sided polygon fractal generator)
import pygame
import random
import math
import tkinter as tk
from tkinter import simpledialog

# initialize pygame
pygame.init()
font = pygame.font.SysFont("Arial", 18)
# set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chaos Game")
# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
# global variables
n_sides = 3  # number of sides of the polygon
iterations = 10000  # number of iterations for the chaos game
fraction = 0.5  # fraction to move towards the vertex
# generate vertices of a regular polygon

def draw_polygon(points, color):
    pygame.draw.polygon(screen, color, points, 1)
def chaos_game(vertices, iterations, fraction):
    # start with a random point inside the polygon
    x = random.uniform(0, WIDTH)
    y = random.uniform(0, HEIGHT)
    for _ in range(iterations):
        # choose a random vertex
        vertex = random.choice(vertices)
        # move towards the vertex by the fraction
        x = (1 - fraction) * x + fraction * vertex[0]
        y = (1 - fraction) * y + fraction * vertex[1]
        # draw the point
        screen.set_at((int(x), int(y)), WHITE)
def ask_input():
    global n_sides, iterations, fraction
    root = tk.Tk()
    root.withdraw()  # hide the main window
    n_sides = simpledialog.askinteger("Input", "Number of sides of the polygon (3-10):", minvalue=3, maxvalue=10)
    iterations = simpledialog.askinteger("Input", "Number of iterations for the chaos game (1000-100000):", minvalue=1000, maxvalue=100000)
    fraction = simpledialog.askfloat("Input", "Fraction to move towards the vertex (0.1-0.9):", minvalue=0.1, maxvalue=0.9)
def main():
    running = True
    vertices = []

    # user input for sides, iterations, and fraction (use a tkinter dialog)
    ask_input()


    for i in range(n_sides):
        angle = 2 * math.pi * i / n_sides
        x = WIDTH // 2 + 200 * math.cos(angle)
        y = HEIGHT // 2 + 200 * math.sin(angle)
        vertices.append((x, y))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # reset the game
                    screen.fill(BLACK)
                    draw_polygon(vertices, RED)
                    chaos_game(vertices, iterations, fraction)
                    pygame.display.flip()
                
        screen.fill(BLACK)
        draw_polygon(vertices, random.choice([RED, GREEN, BLUE, YELLOW]))
        chaos_game(vertices, iterations, fraction)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
