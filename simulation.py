import pygame
import random

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
building = Building(levels=5)

# create random elevators
random_elevators = []
for i in range(random.randint(3,8)):
    random_elevator = Elevator(capacity=random.randint(300, 2500), speed=10)
    random_elevator.level = random.randint(0, building.levels-1)
    random_elevators.append(random_elevator)

# create elevator controller
test_ec = ElevatorController(elevators=random_elevators)

# === game loop ===
running = True
while running:
    # exit when closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -- draw each level --
    for i in range(building.levels):
        level_rect = pygame.Rect(0, height - (i+1) * Building.level_height, width, Building.level_height)
        pygame.draw.rect(screen, (100, 100, 100) if i % 2 == 0 else (50, 50, 50), level_rect)
    
    # -- elevator stuff --
    # calculate the width all elevators (including margins) need
    total_elevator_width = 0
    margin_x = 20   # 20px space between elevators
    for e in test_ec.elevators:
        total_elevator_width += e.width
    total_elevator_width += (len(test_ec.elevators) - 1) * margin_x

    # draw the elevators according to their stats
    offset_x = 0
    for i in range(len(test_ec.elevators)):
        # create pygame rect
        elevator_rect = pygame.Rect(width // 2 - total_elevator_width // 2 + offset_x, height - Building.level_height * test_ec.elevators[i].level - Elevator.height, test_ec.elevators[i].width, Elevator.height)

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
