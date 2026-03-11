import pygame
import random
import math

# custom scripts
from elevator import Elevator
from elevator_controller import ElevatorController
from passenger import Passenger
from building import Building


# === sim setup methods ===
def create_random_elevators(building: Building, margin_x: int=20) -> [Elevator]:
    """
    Creates and returns a list of random elevator objects.
    What it does:
        - random capacity (big or small elevator)
        - random travel speed
        - random start level
        - random start direction
    Also creates a pygame rect used to draw the elevator.
    """
    random_elevators = []
    offset_x = 0
    for i in range(random.randint(7, 7)):
        # instantiate the elevator
        random_elevator = Elevator(capacity=random.randint(300, 2500), speed=200)
        random_elevator.level = random.randint(0, building.levels-1)
        
        # instantiate the pygame part
        random_elevator.graphics = pygame.Rect(offset_x, height - Building.level_height * random_elevator.level - Elevator.height, random_elevator.width, Elevator.height)
        offset_x += random_elevator.width + margin_x

        # give it a random target level
        random_elevator.set_target(target_level=random.randint(0, building.levels-1), building=building)

        random_elevators.append(random_elevator)
    return random_elevators

def get_total_elevator_width(elevators: [Elevator], margin_x: int=20) -> int:
    """
    Takes a list of elevators and the margin between each of them in px.
    Then calculates the width all of the elevators need (x-axis)
    and returns it.
    """
    total_elevator_width = 0
    for e in elevators:
        total_elevator_width += e.graphics.width
    total_elevator_width += margin_x * (len(elevators)-1)
    return total_elevator_width

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
building = Building(levels=6, bottom_y=height)
for i in range(building.levels):
    building.graphics.append(pygame.Rect(0, building.bottom_y - (i+1)\
    * Building.level_height, width, Building.level_height))

# list of randomly generated elevator objects
random_elevators = create_random_elevators(building=building)

# calculate the width all elevators occupy
total_elevator_width = get_total_elevator_width(random_elevators)

# create elevator controller
elevator_controller = ElevatorController(elevators=random_elevators)

# create a line seperating elevators and rest
seperator_line_rect = pygame.Rect(total_elevator_width, 0, 20, height) 

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

    elevator_controller.update_elevators(dt=dt, building=building)


    # === draw ===

    # draw each level 
    for i in range(len(building.graphics)):
        pygame.draw.rect(screen, (30, 30, 30) if i % 2 == 0 else (50, 50, 50), building.graphics[i])

    # draw the elevators
    for e in random_elevators:
        pygame.draw.rect(screen, (255, 255, 255), e.graphics)

    # draw a line seperating elevators and rest of level
    pygame.draw.rect(screen, (200, 200, 200), seperator_line_rect)

    # draw the window
    pygame.display.flip()

pygame.quit()
