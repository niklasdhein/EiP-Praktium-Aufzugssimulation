from level import Level

import pygame
import random

class Building:
    def __init__(self, level_count: int, bottom_y: int, width: int) -> None:
        self.width = width          # width of building
        self.bottom_y = bottom_y    # y-coordinate of the bottom edge 

        self.levels = []                    # reference to the level graphics
        self.regular_levels = []            
        self.level_count = level_count
        self.ground_level = None
        self.bunker_elevator_level = None
        self.create_levels()

        self.elevator_controller = None     # reference to the elevator controller the building contains
        self.staircase = None               # reference to the staircase the building contains

    def get_bunker_levels(self):
        bunker_levels = []
        for level in self.levels:
            if level.level_type != "bunker":
                return bunker_levels
            bunker_levels.append(level)

    def create_levels(self) -> None:
        # spawn bunker only if 3 levels are able to exist (bunker, basement, ground)
        while random.random() <= 0.4 and self.level_count - len(self.levels) >= 3:
            bunker_level = Level(building=self, level=len(self.levels), level_type="bunker")
            self.levels.append(bunker_level)
        
        # pick a random available level for the ground level
        ground_level_level = random.randint(len(self.levels) + 1, self.level_count - 1)
        ground_level = Level(building=self, level=ground_level_level, level_type="ground")

        # when a bunker was generated, create the basement between bunker and ground floor
        # if no bunker was generated, create the basement from bottom up to ground floor
        for i in range(self.levels[-1].level + 1 if len(self.levels) > 0 else 0, ground_level_level):
            basement_level = Level(building=self, level=i, level_type="basement")
            self.levels.append(basement_level)

        # if a bunker exists find the basement level which contains the bunker elevator
        if self.levels[0].level_type == "bunker":
            for level in self.levels:
                if level.level_type == "basement":
                    self.bunker_elevator_level = level
                    break
        
        # append ground level after basement levels
        self.levels.append(ground_level)
        self.ground_level = ground_level

        # pick a random placement if possible for penthouse levels
        first_possible_penthouse_level = ground_level_level + 2
        penthouse_levels = []
        if first_possible_penthouse_level <= self.level_count - 1:
            penthouse_start_level = random.randint(first_possible_penthouse_level, self.level_count - 1)
            for i in range(penthouse_start_level, self.level_count):
                penthouse_levels.append(Level(building=self, level=i, level_type="penthouse"))

        # generate upstairs levels if space for them is left
        if ground_level_level < self.level_count - 1:
            for i in range(ground_level_level + 1, self.level_count - len(penthouse_levels)):
                upstairs_level = Level(building=self, level=i, level_type="upstairs")
                self.levels.append(upstairs_level)
        
        # append the penthouse levels after the normal upstairs levels
        self.levels += penthouse_levels

        # extract all regular levels for better handling for normal people and elevators
        for level in self.levels:
            if level.level_type in ["basement", "ground", "upstairs"]:
                self.regular_levels.append(level)

        print("--- building (all levels) ---")
        for i in range(len(self.levels) - 1, -1, -1):
            print(f"[ {i} ] {self.levels[i].level_type}")