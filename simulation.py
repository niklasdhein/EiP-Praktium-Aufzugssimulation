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
    elevator_count: int=6, 
    level_count: int=5,
    big_elevator_spawn_probability: float=0.3,
    elevator_mode: str="algorithm",     # algorithm, random, pingpong      
    passenger_spawn_chance: float=5,    # probability / second
    passenger_patience: int=25,         # seconds
    speed_multiplier: int=10
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
    elevator_count=elevator_count,
    big_elevator_spawn_probability=big_elevator_spawn_probability,
    elevator_mode=elevator_mode
    )
    building.elevator_controller = elevator_controller

    # prepare list to store spawned passengers in
    passengers = []


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

        # spawn passengers
        if random.random() <= passenger_spawn_chance * dt:
            random_start_level = building.levels[random.randint(0, building.level_count-1)]
            random_target_level = random_start_level
            while random_target_level == random_start_level:
                random_target_level = building.levels[random.randint(0, building.level_count-1)]
            passengers.append(Passenger(current_level=random_start_level,
            target_level=random_target_level,
            weight=80,
            walk_speed=200,
            patience=passenger_patience,
            speed_multiplier=speed_multiplier))

        # handle elevator updates
        elevator_controller.update(dt=dt)

        # handle passenger updates
        for passenger in passengers:
                passenger.update(dt=dt)


        # === draw ===

        # draw each level 
        for i in range(len(building.levels)):
            pygame.draw.rect(screen, (30, 30, 30) if i % 2 == 0 else (50, 50, 50), building.levels[i].background_gfx)
            for elevator in elevator_controller.elevators[:-1]:
                pygame.draw.polygon(screen, 
                (0, 0, 0) if not building.levels[i].up_pressed else (200, 0, 0),
                [
                    (elevator.graphics.x+elevator.graphics.width+(elevator_controller.elevator_margin_x-40)/2, 
                    building.levels[i].background_gfx.y+100),
                    (elevator.graphics.x+elevator.graphics.width+20+(elevator_controller.elevator_margin_x-40)/2, 
                    building.levels[i].background_gfx.y+100),
                    (elevator.graphics.x+elevator.graphics.width+10+(elevator_controller.elevator_margin_x-40)/2, 
                    building.levels[i].background_gfx.y+75)
                ])
                pygame.draw.polygon(screen,
                (0, 0, 0) if not building.levels[i].down_pressed else (200, 0, 0),
                [    
                    (elevator.graphics.x+elevator.graphics.width+20+(elevator_controller.elevator_margin_x-40)/2, 
                    building.levels[i].background_gfx.y+75),
                    (elevator.graphics.x+elevator.graphics.width+40+(elevator_controller.elevator_margin_x-40)/2, 
                    building.levels[i].background_gfx.y+75),
                    (elevator.graphics.x+elevator.graphics.width+30+(elevator_controller.elevator_margin_x-40)/2, 
                    building.levels[i].background_gfx.y+100)
                ]
                )

        # draw the elevators
        for e in elevator_controller.elevators:
            pygame.draw.rect(screen, 
            (255, 255, 255) if e.target_level != None else (0, 0, 200), 
            e.graphics)

        # draw passenger
        for passenger in passengers:
            color = None
            if passenger.states["walking"] :
                if passenger.current_level != passenger.target_level:
                    if not passenger.states["annoyed"]:
                        color = (100, 0, 0)
                    else:
                        color = (255, 0, 0)
                else:
                    color = (0, 200, 0)
            elif passenger.states["elevator_called"]: 
                color = (0, 0, 200)
            else:
                color = (0, 0, 0)
            pygame.draw.rect(screen, color, passenger.graphics)

        # draw onto window
        pygame.display.flip()
    pygame.quit()


# === vars ===

width = 1800
height = 1500


# check if running as main
if __name__ == "__main__":
    start_simulation()