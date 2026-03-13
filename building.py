from level import Level

import pygame

class Building:
    def __init__(self, level_count: int, bottom_y: int, width: int) -> None:
        self.width = width          # width of building
        self.bottom_y = bottom_y    # y-coordinate of the bottom edge 

        self.levels = []                    # Reference to the level graphics
        self.create_levels(level_count)
        self.level_count = len(self.levels)

        self.elevator_controller = None     # reference to the elevator controller the building contains
        self.staircase = None               # reference to the staircase the building contains
        
    def create_levels(self, level_count: int) -> None:
        """
        This function is most likely called on init and creates the
        levels as pygame rects and appends these to the graphics
        array. 
        """
        for i in range(level_count):
            self.levels.append(Level(self, i))