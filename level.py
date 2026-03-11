import pygame

class Level:
    height = 250
    def __init__(self, building: Building, level: int) -> None:
        self.building = building    # building the level belongs to
        self.level = level          # level of the level
        
        self.passengers = None      # list of passengers in the level

        self.graphics = pygame.Rect(0, self.building.bottom_y - (self.level+1) * self.height,\
            self.building.width, self.height)