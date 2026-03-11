import pygame
import random
import math

# custom scripts
from elevator import Elevator
from elevator_controller import ElevatorController
from passenger import Passenger
from building import Building


# === vars ===

width = 1800
height = 1500 

# initialize pygame
pygame.init()

# set appearance
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


# == pre sim stuff ==

# create the building to simulate
building = Building(levels=5, bottom_y=height, width=width)

# create elevator controller
elevator_controller = ElevatorController(building=building)

# create a line seperating elevators and rest
seperator_line_rect = pygame.Rect(elevator_controller.get_total_elevators_width(), 0, 20, height) 

# === game loop ===

running = True
while running:
    # calculates delta time
    dt = clock.tick(60) / 1000.0
    # print(f"FPS: {1/dt}")

    # exit when closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # === calculations ===

    elevator_controller.update_elevators(dt=dt)


    # === draw ===

    # draw each level 
    for i in range(len(building.graphics)):
        pygame.draw.rect(screen, (30, 30, 30) if i % 2 == 0 else (50, 50, 50), building.graphics[i])

    # draw the elevators
    for e in elevator_controller.elevators:
        pygame.draw.rect(screen, (255, 255, 255), e.graphics)

    # draw a line seperating elevators and rest of level
    pygame.draw.rect(screen, (200, 200, 200), seperator_line_rect)

    # draw the window
    pygame.display.flip()
pygame.quit()
