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

# create the levels as rects.
# creates rects each stretching complete x length width fixed height set in building.py.
# the levels are stacked from bottom to top.
level_rects = []
for i in range(building.levels):
    level_rects.append(pygame.Rect(0, height - (i+1) * Building.level_height, width, Building.level_height))

# create random elevator objects
random_elevators = []
for i in range(random.randint(1, 5)):
    random_elevator = Elevator(capacity=random.randint(300, 2500), speed=10)
    random_elevator.level = random.randint(0, building.levels-1)
    random_elevators.append(random_elevator)

# calculate the width all elevators occupy
margin_x = 20   # leave 20px space between elevators
total_elevator_width = 0
for r in random_elevators:
    total_elevator_width += r.width
total_elevator_width += margin_x * (len(random_elevators)-1)

# create elevator controller
elevator_controller = ElevatorController(elevators=random_elevators)

# create a line seperating elevators and rest
seperator_line_rect = pygame.Rect(total_elevator_width, 0, 20, height) 


# === game loop ===
running = True
while running:
    # calculates delta time
    dt = clock.tick(60) / 1000.0

    # exit when closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -- draw each level --
    for i in range(len(level_rects)):
        pygame.draw.rect(screen, (30, 30, 30) if i % 2 == 0 else (50, 50, 50), level_rects[i])
    
    # -- elevator stuff --
    # get all elevators the controller contains and draw them next to each other.
    # draw big elevators double as wide as normal ones.
    # keeps a small margin between them, calculated before the sim starts.
    offset_x = 0
    elevator_rects = []
    for i in range(len(elevator_controller.elevators)):
        # create pygame rect
        elevator_rects.append(pygame.Rect(offset_x, height - Building.level_height * elevator_controller.elevators[i].level - Elevator.height, elevator_controller.elevators[i].width, Elevator.height))

        # calculate offset
        offset_x += elevator_controller.elevators[i].width + margin_x

    # draw the elevators
    for e in elevator_rects:
        pygame.draw.rect(screen, (255, 255, 255), e)

    # draw a line seperating elevators and rest of level
    pygame.draw.rect(screen, (200, 200, 200), seperator_line_rect)

    # draw the window
    pygame.display.flip()

pygame.quit()
