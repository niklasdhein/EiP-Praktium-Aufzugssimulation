import pygame

class Level:
    def __init__(self, building: Building, level: int) -> None:
        self.building = building    # building the level belongs to
        self.level = level          # level of the level
        self.up_pressed = False     # tracks if someone pressed up 
        self.down_pressed = False   # or down button for elevator
        
        self.passengers = []        # list of passengers in the level

        self.graphics = pygame.Rect(0, self.building.bottom_y - (self.level+1) * 250,\
            self.building.width, 250)

    def call_elevator_up(self) -> None:
        self.up_pressed = True

    def call_elevator_down(self) -> None:
        self.down_pressed = True