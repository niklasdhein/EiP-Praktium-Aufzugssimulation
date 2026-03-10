import pygame

# === vars ===
width = 800
height = 600

# initialize pygame
pygame.init()

# set appearance
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# -- game loop -- 
running = True
while running:
    # exit when closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the window
    pygame.display.flip()

    # 60 fps limit
    clock.tick(60)

pygame.quit()
