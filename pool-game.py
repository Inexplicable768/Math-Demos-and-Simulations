import math
import random
import pygame as pg


class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.color = self.get_random_color()
        self.radius = radius
        self.velocity_x = 0
        self.velocity_y = 0
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # Keep the ball within the table boundaries
        self.x = max(self.radius, min(self.x, 800 - self.radius))
        self.y = max(self.radius, min(self.y, 400 - self.radius))
    def collides_with(self, other):
        distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return distance < self.radius + other.radius
    def get_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def draw(self, surface):
        pg.draw.circle(surface, self.color , (int(self.x), int(self.y)), self.radius)

class Pocket:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    def contains(self, ball):
        distance = ((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2) ** 0.5
        return distance < self.radius
    def draw(self, surface):
        pg.draw.circle(surface, (0, 0, 0), (int(self.x), int(self.y)), self.radius)

class PoolTable:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.balls = []
        self.pockets = []
        self.friction = 0.98
        self.borders = [(0, 0, width, 0), (width, 0, width, height), (width, height, 0, height), (0, height, 0, 0)]
    def add_ball(self, ball):
        self.balls.append(ball)
    def add_pocket(self, pocket):
        self.pockets.append(pocket)
    def update(self):
        for ball in self.balls:
            ball.x += ball.velocity_x
            ball.y += ball.velocity_y
            ball.velocity_x *= self.friction
            ball.velocity_y *= self.friction
        for ball in self.balls:
            for other in self.balls:
                if ball != other and ball.collides_with(other):
                    # Handle collision (simplified)
                    ball.move(-1, -1)  # Move back to avoid overlap
            for pocket in self.pockets:
                if pocket.contains(ball):
                    self.balls.remove(ball)
    def draw(self, surface):
        surface.fill((0, 128, 0))  # Green table
        for pocket in self.pockets:
            pocket.draw(surface)
        for ball in self.balls:
            ball.draw(surface)
def main():
    pg.init()
    screen = pg.display.set_mode((800, 400))
    pg.display.set_caption("Pool Game Physics Simulation")
    clock = pg.time.Clock()
    table = PoolTable(800, 400)
    # draw pool triangle
    # start at 5 balls in the first row, then 4, 3, 2, 1
    for i in range(5):
        for j in range(i + 1):
            table.add_ball(Ball(200 + i * 28, table.height // 2 + j * 28 - i * 14, 14))

    table.add_pocket(Pocket(50, 50, 20))
    table.add_pocket(Pocket(400, 50, 20))
    table.add_pocket(Pocket(750, 50, 20))

    table.add_pocket(Pocket(50, 350, 20))
    table.add_pocket(Pocket(400, 350, 20))
    table.add_pocket(Pocket(750, 350, 20))
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            # shoot the ball by dragging the mouse
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                for ball in table.balls:
                    if ((ball.x - mouse_x) ** 2 + (ball.y - mouse_y) ** 2) ** 0.5 < ball.radius:
                        ball.velocity_x = (mouse_x - ball.x) * 0.1
                        ball.velocity_y = (mouse_y - ball.y) * 0.1
                        
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    for ball in table.balls:
                        ball.velocity_x = 0
                        ball.velocity_y = 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    table.balls.clear()
                    for i in range(5):
                        for j in range(i + 1):
                            table.add_ball(Ball(200 + i * 20, table.height // 2 + j * 20 - i * 10, 10))
        table.update()
        table.draw(screen)
        pg.display.flip()
        clock.tick(60)
    pg.quit()
if __name__ == "__main__":    
    main()
