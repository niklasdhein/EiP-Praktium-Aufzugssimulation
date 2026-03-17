import pygame

class Level:
    def __init__(self, building: Building, level: int) -> None:
        self.building = building    # building the level belongs to
        self.level = level          # level of the level
        self.up_pressed = False     # tracks if someone pressed up 
        self.down_pressed = False   # or down button for elevator
        
        self.passengers = []        # list of passengers in the level

        height = self.building.bottom_y / self.building.level_count
        self.background_gfx = pygame.Rect(
            0, 
            self.building.bottom_y - (self.level+1) * height,
            self.building.width, 
            height
        )

        # statistics variables
        self.passengers_annoyed = 0

    def remove_passenger_from_level(self, passenger: Passenger) -> None:
        new_passengers = []
        for p in self.passengers:
            if p != passenger: 
                new_passengers.append(p)
        self.passengers = new_passengers

    def call_elevator_up(self) -> None:
        self.up_pressed = True

    def call_elevator_down(self) -> None:
        self.down_pressed = True