#! ./.venv/bin/python

import pygame
import random
import math
import json
import os

# custom scripts
from elevator import Elevator
from elevator_controller import ElevatorController
from passenger import Passenger
from codsworth import Codsworth
from building import Building
import statistics


# === vars ===

width = 2000
height = 1500
target_framerate = 60
use_config = False


# === simulation method(s) ===

def get_config_from_file(file_path: str="./config.json", print_config: bool=False) -> dict:
    # return if file doesn't exists
    if not os.path.exists(file_path):
        return

    # load the config
    loaded_config = {}
    with open(file_path) as f:
        loaded_config = json.load(f)

    # show config
    if print_config:
        print("== loaded config ==")
        for key in loaded_config:
            print(f"{key}:\t{loaded_config[key]}")
        print("==  config end   ==")

    return loaded_config

def start_simulation(
    elevator_count: int=3, 
    level_count: int=5,
    big_elevator_spawn_probability: float=0.3,
    elevator_mode: str="algorithm",     # algorithm, random, pingpong      
    passenger_spawn_chance: float=1,    # probability / second
    passenger_patience: int=25,         # seconds
    speed_multiplier: int=3,
    simulation_time: int=3600           #seconds
    ) -> None:


    # == methods used in the simulation ==  

    def spawn_passenger(passengers: list) -> bool:
        """
        Spawns to a certain chance a passenger and appends it to the
        passed array. Also returns wether spawning was a success or not.
        """
        # probabilty a passenger gets spawned
        if random.random() <= passenger_spawn_chance * speed_multiplier * dt:
            prob = random.random()
            # spawn on base level (60% chance)
            if random.random() <= 0.6:
                start_level = building.ground_level
            # spawn on other random level
            else:
                start_level = building.regular_levels[random.randint(0, len(building.regular_levels) - 1)]
            # choose a valid target (not the same as the start level)
            target_level = start_level
            while target_level == start_level:
                target_level = building.regular_levels[random.randint(0, len(building.regular_levels) - 1)]

            # probability codsworth gets spawned
            if prob > 0.8 and prob <= 0.9 and building.bunker_elevator_level != None:
                start_level = building.ground_level
                bunker_levels = building.get_bunker_levels()
                target_level = bunker_levels[random.randint(0, len(bunker_levels) - 1)]
                passengers.append(
                    Codsworth(
                        current_level=start_level,
                        target_level=target_level,
                        bunker_elevator_level=building.bunker_elevator_level,
                        weight=80,
                        walk_speed=200,
                        patience=passenger_patience,
                        use_sprite=use_sprite,
                        entity_scale_factor=entity_scale_factor
                    )
                )

            # probability a vip gets spawned
            elif prob > 0.9 and building.levels[-1].level_type == "penthouse":
                penthouse_levels = building.get_penthouse_levels()
                passengers.append(
                    Passenger(
                        current_level=start_level,
                        target_level=penthouse_levels[random.randint(0, len(penthouse_levels) - 1)],
                        weight=80,
                        walk_speed=200,
                        patience=passenger_patience,
                        use_sprite=use_sprite,
                        entity_scale_factor=entity_scale_factor
                    )
                )

            # probability a normal passenger gets spawned
            else:
                passengers.append(
                    Passenger(
                        current_level=start_level,
                        target_level=target_level,
                        weight=80,
                        walk_speed=200,
                        patience=passenger_patience,
                        use_sprite=use_sprite,
                        entity_scale_factor=entity_scale_factor
                    )
                )

            return True
        return False

    def draw_building() -> None:
        # draw each level 
        for i in range(building.level_count):
            level = building.levels[i]
            button_width = 20

            # level background
            if level.level_type == "bunker":
                pygame.draw.rect(screen, (0, 0, 0) if i % 2 == 0 else (20, 20, 20), level.background_gfx)
            elif level.level_type == "basement":
                pygame.draw.rect(screen, (30, 30, 30) if i % 2 == 0 else (50, 50, 50), level.background_gfx)
            elif level.level_type == "ground":
                pygame.draw.rect(screen, (100, 100, 100), level.background_gfx)
            elif level.level_type == "upstairs":
                pygame.draw.rect(screen, (150, 150, 150) if i % 2 == 0 else (170, 170, 170), level.background_gfx)
            elif level.level_type == "penthouse":
                pygame.draw.rect(screen, (255, 255, 255) if i % 2 == 0 else (235, 235, 235), level.background_gfx)

            # one elevator
            call_color = (200, 50, 50)
            no_call_color = (0, 0, 0)
            if len(elevator_controller.elevators) == 1:
                elevator = elevator_controller.elevators[0]
                x = elevator.graphics.x + elevator.graphics.width + (elevator_controller.elevator_margin_x - button_width) / 2
                y = level.background_gfx.y + level.background_gfx.height - elevator.graphics.height / 2 

                # up call-button
                pygame.draw.polygon(screen, 
                no_call_color if not building.levels[i].up_pressed else call_color,
                [
                    (x, y),
                    (x + button_width, y), 
                    (x + button_width / 2, y - button_width)
                ])
                # down call-button
                pygame.draw.polygon(screen,
                no_call_color if not building.levels[i].down_pressed else call_color,
                [    
                    (x + button_width, y - button_width),
                    (x + button_width * 2, y - button_width),
                    (x + button_width * 1.5, y)   
                ])
            
            # more than one elevator
            else:    
                for elevator in elevator_controller.elevators[:-1]: 
                    x = elevator.graphics.x + elevator.graphics.width + (elevator_controller.elevator_margin_x - button_width) / 2
                    y = level.background_gfx.y + level.background_gfx.height - elevator.graphics.height / 2
                    
                    # up call-button
                    pygame.draw.polygon(screen, 
                    no_call_color if not building.levels[i].up_pressed else call_color,
                    [
                        (x, y),
                        (x + button_width, y), 
                        (x + button_width / 2, y - button_width)
                    ])

                    # down call-button
                    pygame.draw.polygon(screen,
                    no_call_color if not building.levels[i].down_pressed else call_color,
                    [    
                        (x + button_width, y - button_width),
                        (x + button_width * 2, y - button_width),
                        (x + button_width * 1.5, y)   
                    ])
            
            # draw a direction indicator above every elevator
            for elevator in elevator_controller.elevators:
                elevator_center_x = elevator.graphics.x + elevator.graphics.width // 2
                top_y = building.levels[i].background_gfx.y + 5
                pygame.draw.rect(screen, 
                (0, 0, 0),
                pygame.Rect(elevator_center_x-15, top_y, 30, 30))
                if elevator.direction == 1:
                    pygame.draw.polygon(screen,
                    (200, 0, 0),
                    [
                        (elevator_center_x-12, top_y),
                        (elevator_center_x+12, top_y),
                        (elevator_center_x, top_y+20)
                    ])
                elif elevator.direction == -1:
                    pygame.draw.polygon(screen,
                    (0, 200, 0),
                    [
                        (elevator_center_x-12, top_y+30),
                        (elevator_center_x+12, top_y+30),
                        (elevator_center_x, top_y+10)
                    ])

    def draw_elevators() -> None:
        # draw the elevators
        for e in elevator_controller.elevators:
            if not e.use_sprite:
                # draw each elevator
                pygame.draw.rect(screen,
                (255, 255, 255) if e.target_level != None else (0, 0, 200),
                e.graphics)

                # draw door
                pygame.draw.rect(screen, (0, 0, 0), e.door)
            else:
                screen.blit(
                    e.shown_surface, e.graphics
                )

    def draw_passengers() -> None:  
        # draw passenger
        for passenger in passengers:
            if not passenger.visible: continue

            # in case sprites are used
            if passenger.use_sprite:
                if passenger.walk_direction != 0:
                    if passenger.current_level != passenger.target_level:
                        if passenger.walk_direction == -1 and not passenger.states["annoyed"]:
                            screen.blit(
                                passenger.left_loaded_surfaces[passenger.shown_surface_index], passenger.graphics
                            )
                        elif passenger.walk_direction == -1 and passenger.states["annoyed"]:
                            pass    # no animation yet

                        elif passenger.walk_direction == 1 and not passenger.states["annoyed"]:
                            screen.blit(
                                passenger.right_loaded_surfaces[passenger.shown_surface_index], passenger.graphics
                            )
                        elif passenger.walk_direction == 1 and passenger.states["annoyed"]:
                            screen.blit(
                                passenger.bad_right_loaded_surfaces[passenger.shown_surface_index], passenger.graphics
                            )

                    else:
                        if passenger.walk_direction == -1:
                            screen.blit(
                                passenger.good_left_loaded_surfaces[passenger.shown_surface_index], passenger.graphics
                            )
                        elif passenger.walk_direction == 1:
                            screen.blit(
                                passenger.good_right_loaded_surfaces[passenger.shown_surface_index], passenger.graphics
                            )
                else:
                    screen.blit(
                        passenger.idle_loaded_surfaces[passenger.shown_surface_index], passenger.graphics
                    )

            # in case rectangles are used
            else:
                color = None
                if passenger.states["walking"]:
                    if passenger.current_level != passenger.target_level:
                        if not passenger.states["annoyed"]:
                            color = (200, 0, 200)
                        else:
                            color = (255, 0, 0)
                    else:
                        color = (0, 200, 0)
                elif passenger.states["elevator_called"]: 
                    color = (0, 0, 200)
                else:
                    color = (0, 0, 200)
                pygame.draw.rect(screen, color, passenger.graphics)


    # == before setup ==

    # default values for config specific settings
    use_sprite = False
    entity_scale_factor = 1

    # load and use config, when said
    if use_config:
        loaded_config = get_config_from_file(file_path="./config.json", print_config=True)

        elevator_count = loaded_config["elevator_count"]
        level_count = loaded_config["level_count"]
        big_elevator_spawn_probability = loaded_config["big_elevator_spawn_probability"]
        elevator_mode = loaded_config["elevator_mode"]
        passenger_spawn_chance = loaded_config["passenger_spawn_chance"]
        passenger_patience = loaded_config["passenger_patience"]
        speed_multiplier = loaded_config["speed_multiplier"]
        simulation_time = loaded_config["simulation_time"]
        use_sprite = loaded_config["use_sprite"]
        entity_scale_factor = loaded_config["entity_scale_factor"]


    # == pre sim stuff ==

    # initialize pygame
    pygame.init()

    # set appearance
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # create the building to simulate
    building = Building(level_count=level_count, bottom_y=height, width=width)

    # create elevator controller
    elevator_controller = ElevatorController(
    building=building, 
    elevator_count=elevator_count,
    big_elevator_spawn_probability=big_elevator_spawn_probability,
    elevator_mode=elevator_mode,
    use_sprite=use_sprite,
    entity_scale_factor=entity_scale_factor
    )
    building.elevator_controller = elevator_controller

    # prepare list to store spawned passengers in
    passengers = []


    # == statistic variables ==
    passengers_transported = 0
    passengers_annoyed = 0
    passengers_spawned = 0


    # === game loop ===

    running = True
    time_elapsed = 0
    while running:
        # calculates delta time
        dt = clock.tick(target_framerate) / 1000.0
        # print(f"FPS: {1/dt}")

        # exit when closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        # exit when runtime is over
        time_elapsed += dt
        if time_elapsed >= simulation_time: running = False


        # === calculations ===

        # spawns with probability a passenger
        if spawn_passenger(passengers=passengers): passengers_spawned += 1

        # handle elevator updates
        elevator_controller.update(dt=dt, speed_multiplier=speed_multiplier)

        # handle passenger updates
        for passenger in passengers:
            passenger.update(dt=dt, speed_multiplier=speed_multiplier)


        # === draw ===

        draw_building()
        draw_elevators()
        draw_passengers()

        # draw on window
        pygame.display.flip()

    pygame.quit()

    print(f"simulation exited. {time_elapsed:.3f}s elapsed.")

    # some statistics work
    for e in elevator_controller.elevators:
        passengers_transported += e.passengers_transported
    for l in building.levels:
        passengers_annoyed += l.passengers_annoyed
    
    print(f"\n--- statistics ---\
        \ntransported:\t{passengers_transported} ({passengers_transported/passengers_spawned*100:.2f}%)\
        \nannoyed:\t{passengers_annoyed} ({passengers_annoyed/passengers_spawned*100:.2f}%)\
        \nspawned:\t{passengers_spawned}\n\
        \nelevator mode:\t{elevator_mode}")
    print("\nelevators in detail:")
    for i in range(len(elevator_controller.elevators)):
        transported = elevator_controller.elevators[i].passengers_transported
        print(f"elevator {i} ({"small" if elevator_controller.elevators[i].capacity <= 1000 else "big"}):\t{transported} ({transported/passengers_spawned*100:.2f}%)")

    statistics.pie_split(passengers_transported, passengers_annoyed, passengers_spawned)
    statistics.elevator_efficiency(passengers_transported, elevator_controller.elevators)

# check if running as main
if __name__ == "__main__":
    start_simulation()
