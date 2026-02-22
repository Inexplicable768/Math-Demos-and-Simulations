import pygame
import numpy as np # im using numpy for faster pixel manipulation

# Window size
WIDTH, HEIGHT = 800, 600

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mandelbrot Set Explorer")

# Mandelbrot parameters
max_iter = 100
zoom = 1.0
offset_x, offset_y = 0.0, 0.0

# Color function
def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

# Function to draw the Mandelbrot set
# optimized with vectorized numpy operations for better performance so its not a slideshow
# Virtual resolution lower for speed. still looks good
V_WIDTH, V_HEIGHT = 300, 150  # half of the screen resolution

def draw_mandelbrot():
    global screen, zoom, offset_x, offset_y

    # Create a smaller grid
    x = np.linspace(-1.5 / zoom + offset_x, 1.5 / zoom + offset_x, V_WIDTH)
    y = np.linspace(-1.0 / zoom + offset_y, 1.0 / zoom + offset_y, V_HEIGHT)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    M = np.full(C.shape, max_iter, dtype=int)

    mask = np.full(C.shape, True, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask]*Z[mask] + C[mask]
        mask, old_mask = abs(Z) <= 2, mask
        M[mask ^ old_mask] = i

    pixels = 255 - (M * 255 // max_iter)
    # can be modified to use a color palette instead of grayscale if desired
    rgb_array = np.stack([pixels]*3, axis=-1).astype(np.uint8)

    # Transpose for Pygame
    rgb_array = np.transpose(rgb_array, (1, 0, 2))

    # Scale up to the actual screen size
    surface = pygame.surfarray.make_surface(rgb_array)
    surface = pygame.transform.smoothscale(surface, (WIDTH, HEIGHT))

    screen.blit(surface, (0, 0))
    pygame.display.flip()
# Main loop and flag variables
running = True
dragging = False
last_mouse_pos = None
needs_redraw = True

while running:
    if needs_redraw:
        draw_mandelbrot()
        needs_redraw = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in [4, 5]:  # scroll zoom
                zoom *= 1.2 if event.button == 4 else 1 / 1.2
                needs_redraw = True
            elif event.button == 1:
                dragging = True
                last_mouse_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

        elif event.type == pygame.MOUSEMOTION and dragging:
            dx = event.pos[0] - last_mouse_pos[0]
            dy = event.pos[1] - last_mouse_pos[1]
            offset_x -= dx / (0.5 * zoom * WIDTH) * 1.5
            offset_y -= dy / (0.5 * zoom * HEIGHT)
            last_mouse_pos = event.pos
            needs_redraw = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                zoom = 1.0
                offset_x, offset_y = 0.0, 0.0
                needs_redraw = True
                # reset view to default

pygame.quit()