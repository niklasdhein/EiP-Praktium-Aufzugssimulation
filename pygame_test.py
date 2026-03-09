import pygame

# === vars ===
width = 800
height = 600

# initialisiert pygame
pygame.init()

# fenster setup
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# mitte berechnen
center_pos = pygame.Vector2(width // 2, height // 2)

# game loop
running = True
while running:
    # fenster schließen, wenn x
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # weißer hintergrund
    screen.fill("black")

    # roter kreis
    pygame.draw.circle(screen, "red", center_pos, 150)

    # zeichnen
    pygame.display.flip()

    # 60 fps limit
    clock.tick(60)

pygame.quit()
