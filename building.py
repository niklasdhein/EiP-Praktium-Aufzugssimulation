from level import Level

import pygame
import random

class Building:
    def __init__(self, level_count: int, bottom_y: int, width: int) -> None:
        self.width = width          # width of building
        self.bottom_y = bottom_y    # y-coordinate of the bottom edge 

        self.levels = []                    # Reference to the level graphics
        self.level_count = level_count
        self.base_level = None
        self.create_levels()

        self.elevator_controller = None     # reference to the elevator controller the building contains
        self.staircase = None               # reference to the staircase the building contains

    def create_levels(self) -> None:
        """
        This function is most likely called on init and creates the
        levels as pygame rects and appends these to the graphics
        array. 
        """
        for i in range(self.level_count):
            level = Level(building=self, level=i)

            # determine to a random chance if this level is the base level
            if self.base_level == None: 
                if random.random() <= 0.3:
                    self.base_level = level
                    self.base_level.type = "normal"
                else:
                    level.type = "basement"
            else:
                level.type = "normal"

            self.levels.append(level)
        
        # in the unlikely case no base level was randomly chosen,
        # set the highest level as base level
        if self.base_level == None: 
            self.base_level = self.levels[-1]
            self.base_level.type = "normal"