import random
import pygame as pg

# constants
WIDTH, HEIGHT = 800, 600
NUM_PEG_ROWS = 10
BALL_RADIUS = 5
PEG_RADIUS = 5
NUM_BALLS = 200
BIN_WIDTH = WIDTH // (NUM_PEG_ROWS + 1)
PROBABILITY_LEFT = 0.5
BALL_SPEED = 5  # pixels per frame for smoother animation

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# vertical spacing between peg rows
ROW_SPACING = (HEIGHT - 150) // (NUM_PEG_ROWS + 1)  # leave space for bins

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = BALL_RADIUS
        self.peg = 0
        self.finished = False
        self.target_x = self.x
        self.target_y = self.y + ROW_SPACING

    def fall_step(self):
        if self.peg >= NUM_PEG_ROWS:
            self.finished = True
            return

        # move smoothly toward target
        if self.y < self.target_y:
            self.y += BALL_SPEED
        if self.y >= self.target_y:
            # decide left or right
            if random.random() < PROBABILITY_LEFT:
                self.x -= BIN_WIDTH // 2
            else:
                self.x += BIN_WIDTH // 2
            self.peg += 1
            self.target_y += ROW_SPACING

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Galton Board Simulation")
    clock = pg.time.Clock()

    balls = [Ball() for _ in range(NUM_BALLS)]
    bins = [0 for _ in range(NUM_PEG_ROWS + 1)]

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(WHITE)

        # draw pegs
        for row in range(NUM_PEG_ROWS):
            for col in range(row + 1):
                peg_x = WIDTH // 2 - (row * BIN_WIDTH // 2) + col * BIN_WIDTH
                peg_y = (row + 1) * ROW_SPACING
                pg.draw.circle(screen, BLACK, (peg_x, peg_y), PEG_RADIUS)

        # move and draw balls
        for ball in balls:
            if not ball.finished:
                ball.fall_step()
            pg.draw.circle(screen, BLUE, (int(ball.x), int(ball.y)), BALL_RADIUS)

        # update bins
        bins = [0 for _ in range(NUM_PEG_ROWS + 1)]
        for ball in balls:
            if ball.finished:
                idx = int((ball.x + BIN_WIDTH // 2) // BIN_WIDTH)
                idx = max(0, min(NUM_PEG_ROWS, idx))
                bins[idx] += 1

        # draw bins histogram
        max_bin_height = max(bins) if bins else 1
        if max_bin_height > 0:
            for i, count in enumerate(bins):
                bin_x = i * BIN_WIDTH
                bin_height = int((count / max_bin_height) * 150)  # scale relative to max count
                pg.draw.rect(screen, BLACK, (bin_x, HEIGHT - bin_height, BIN_WIDTH, bin_height))

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()