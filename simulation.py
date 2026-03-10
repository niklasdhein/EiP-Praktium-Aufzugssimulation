import pygame
import random

# custom scripts
from elevator import Elevator
from elevator_controller import ElevatorController
from passenger import Passenger

# === vars ===
width = 800
height = 600

# initialize pygame
pygame.init()

# set appearance
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# == pre sim stuff ==

# spawn an elevator
test_elevator1 = Elevator(500, 10)
test_elevator2 = Elevator(1500, 10)
test_elevator3 = Elevator(200, 10)

# create elevator controller
test_ec = ElevatorController([test_elevator1, test_elevator2, test_elevator3])

# === game loop ===
running = True
while running:
    # exit when closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # calculate the expected width of all elevators
    total_elevator_width = 0
    margin_x = 20   # 20px space between elevators
    for e in test_ec.elevators:
        total_elevator_width += e.width
    total_elevator_width += (len(test_ec.elevators) - 1) * margin_x

    # draw each elevator
    offset_x = 0
    for i in range(len(test_ec.elevators)):
        # create pygame rect
        elevator_rect = pygame.Rect(width // 2 - total_elevator_width // 2 + offset_x, height // 2 - Elevator.height // 2, test_ec.elevators[i].width, Elevator.height)

        # calculate offset
        offset_x += test_ec.elevators[i].width + margin_x

        # random color
        # elevator_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        elevator_color = (255, 255, 255)

        # draw
        pygame.draw.rect(screen, elevator_color, elevator_rect)

    # draw the window
    pygame.display.flip()

    # 60 fps limit
    clock.tick(60)

pygame.quit()
