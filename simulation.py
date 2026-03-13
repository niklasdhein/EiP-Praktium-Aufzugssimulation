import pygame
import random
import math

# custom scripts
from elevator import Elevator
from elevator_controller import ElevatorController
from passenger import Passenger
from building import Building


# === simulation method(s) ===

def start_simulation(
    elevator_count: int, 
    level_count: int,
    big_elevator_spawn_probability: float,
    elevator_mode: str,
    passenger_spawn_rate: float,
    passenger_patience: int
    ) -> None:

    # == pre sim stuff ==

    # initialize pygame
    pygame.init()

    # set appearance
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # create the building to simulate
    building = Building(level_count=level_count, bottom_y=height, width=width)

    # create elevator controller
    elevator_controller = ElevatorController(building=building, 
    speed_multiplier=speed_multiplier, 
    elevator_count=elevator_count
    )
    building.elevator_controller = elevator_controller

    # create a line seperating elevators and rest
    seperator_line_rect = pygame.Rect(elevator_controller.get_total_elevators_width(), 0, 20, height) 

    # create a test passenger
    test_passengers = []
    for i in range(70):
        random_start_level = building.levels[random.randint(0, building.level_count-1)]
        random_target_level = -1
        while True:
            random_target_level = building.levels[random.randint(0, building.level_count-1)]
            if random_target_level != random_start_level:
                break
        test_passengers.append(Passenger(current_level=random_start_level,\
            target_level=random_target_level, walk_speed=200*speed_multiplier))


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

        elevator_controller.update(dt=dt)
        for passenger in test_passengers:
                passenger.update(dt=dt)


        # === draw ===

        # draw each level 
        for i in range(len(building.levels)):
            pygame.draw.rect(screen, (30, 30, 30) if i % 2 == 0 else (50, 50, 50), building.levels[i].background_gfx)
            pygame.draw.polygon(screen, 
            (0, 0, 0) if not building.levels[i].up_pressed else (200, 0, 0),
            [
                (elevator_controller.get_total_elevators_width()+100, 
                building.levels[i].background_gfx.y+80),
                (elevator_controller.get_total_elevators_width()+120, 
                building.levels[i].background_gfx.y+80),
                (elevator_controller.get_total_elevators_width()+110, 
                building.levels[i].background_gfx.y+55)
            ])
            pygame.draw.polygon(screen,
            (0, 0, 0) if not building.levels[i].down_pressed else (200, 0, 0),
            [    
                (elevator_controller.get_total_elevators_width()+120, 
                building.levels[i].background_gfx.y+55),
                (elevator_controller.get_total_elevators_width()+140, 
                building.levels[i].background_gfx.y+55),
                (elevator_controller.get_total_elevators_width()+130, 
                building.levels[i].background_gfx.y+80)
            ]
            )

        # draw the elevators
        for e in elevator_controller.elevators:
            pygame.draw.rect(screen, 
            (255, 255, 255) if e.target_level != None else (0, 0, 200), 
            e.graphics)

        # draw a line seperating elevators and rest of level
        pygame.draw.rect(screen, (200, 200, 200), seperator_line_rect)

        # draw passenger
        for passenger in test_passengers:
            color = None
            if passenger.states["walking"] and passenger.current_level != passenger.target_level: 
                color = (200, 0, 0)
            elif passenger.states["elevator_called"]: 
                color = (0, 0, 200)
            elif passenger.states["walking"] and passenger.current_level == passenger.target_level:
                color = (0, 200, 0)
            else:
                color = (0, 0, 0)
            pygame.draw.rect(screen, color, passenger.graphics)

        # draw onto window
        pygame.display.flip()
    pygame.quit()


# === vars ===

width = 1800
height = 1500
speed_multiplier = 5