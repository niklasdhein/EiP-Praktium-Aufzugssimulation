import pygame

class Building:
    level_height = 250
    def __init__(self, levels: int, bottom_y: int, width: int) -> None:
        self.width = width          # width of building
        self.levels = levels        # amount of levels the building contains
        self.height = self.level_height * self.levels   # building height in px
        self.bottom_y = bottom_y    # y-coordinate of the bottom edge 

        self.elevator_controller = None     # reference to the elevator controller the building contains
        self.staircase = None               # reference to the staircase the building contains

        self.graphics = []          # Reference to the level graphics

        self.create_levels()
        
    def create_levels(self) -> None:
        """
        This function is most likely called on init and creates the
        levels as pygame rects and appends these to the graphics
        array. 
        """
        for i in range(self.levels):
            self.graphics.append(pygame.Rect(0, self.bottom_y - (i+1)\
            * self.level_height, self.width, self.level_height))