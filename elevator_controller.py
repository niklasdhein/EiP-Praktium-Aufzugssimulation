import random
import pygame

from elevator import Elevator
from building import Building

class ElevatorController:
    def __init__(self, building: Building) -> None:
        self.building = building    # parent building
        self.elevators = []         # children elevators

        self.create_random_elevators()  # fills self.elevators

        self.call_buttons = {}
        for i in range(self.building.levels):
            self.call_buttons[i] = {
                "up": False,
                "down": False
                }
        
        # hardcode
        self.call_buttons[4]["up"] = True

    def update_elevators(self, dt: float) -> None:
        """
        The controller is like the head control-unit of all elevators.
        """

        # check for new elevator calls
        for i in self.call_buttons:
            if self.call_buttons[i]["up"]: 
                print(f"Person in Etage {i} möchte nach oben.")
                self.elevators[0].set_target(target_level=i)
                self.call_buttons[i]["up"] = False
            elif self.call_buttons[i]["down"]: 
                print(f"Person in Etage {i} möchte nach unten.")
                self.elevators[0].set_target(target_level=i)
                self.call_buttons[i]["down"] = False

        # move elevators
        for elevator in self.elevators:
            if elevator.target_level != None:
                elevator.move_to_target(dt)

    def create_random_elevators(self, margin_x: int=20) -> None:
        """
        Creates random elevators and set these as children of
        the controller.
        """
        offset_x = 0
        for i in range(random.randint(1, 1)):
            # instantiate the elevator
            random_elevator = Elevator(elevator_controller=self, capacity=random.randint(300, 2500), speed=200)
            random_elevator.level = random.randint(0, self.building.levels-1)
            
            # instantiate the pygame part
            random_elevator.graphics = pygame.Rect(offset_x, self.building.bottom_y - Building.level_height\
                * random_elevator.level - Elevator.height, random_elevator.width, Elevator.height)
            offset_x += random_elevator.width + margin_x

            # give it a random target level
            random_elevator.set_target(target_level=random.randint(0, self.building.levels-1))

            self.elevators.append(random_elevator)

    def get_total_elevators_width(self, margin_x: int=20) -> int:
        """
        Calculates the width in px all elevators need and
        returns it.
        """
        width = 0
        for elevator in self.elevators:
            width += elevator.graphics.width
        width += margin_x * (len(self.elevators)-1)
        return width