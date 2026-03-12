import random
import pygame

from elevator import Elevator
from building import Building

class ElevatorController:
    def __init__(self, building: Building) -> None:
        self.building = building    # parent building
        self.elevators = []         # children elevators

        self.create_random_elevators()  # fills self.elevators

        # stores all elevator calls from all levels.
        # the calls are seperated in up and down calls for later
        # optimization.
        self.elevator_calls = {
            "up": [],
            "down": []
        }

    def update(self, dt: float) -> None:
        """
        The controller is like the head control-unit of all elevators.
        """

        self.check_for_new_calls()
        self.try_to_send_elevator_to_call()
        self.let_all_elevators_move(dt=dt)

    def let_all_elevators_move(self, dt: float) -> None:
        # move elevators if they have a target
        for elevator in self.elevators:
            if elevator.target_level != None:
                elevator.move_to_target(dt)

    def create_random_elevators(self, margin_x: int=20) -> None:
        """
        Creates random elevators and set these as children of
        the controller.
        """
        offset_x = 0
        for i in range(random.randint(2, 2)):
            # instantiate the elevator
            random_elevator = Elevator(elevator_controller=self, capacity=random.randint(300, 2500), speed=200)
            random_elevator.level = random.randint(0, self.building.level_count-1)
            
            # instantiate the pygame part
            random_elevator.graphics = pygame.Rect(offset_x, self.building.bottom_y - self.building.levels[0].graphics.height\
                * random_elevator.level - 200, random_elevator.width, 200)
            offset_x += random_elevator.width + margin_x

            self.elevators.append(random_elevator)

    def try_to_send_elevator_to_call(self) -> None:
        # handle which elevator travels to which floor
        for i in range(len(self.elevator_calls["up"])):
            for elevator in self.elevators:
                if len(elevator.queue) == 0:
                    elevator.add_to_queue(self.elevator_calls["up"][i])
                    self.elevator_calls["up"].pop(i)
                    break

        for i in range(len(self.elevator_calls["down"])):
            for elevator in self.elevators:
                if len(elevator.queue) == 0:
                    elevator.add_to_queue(self.elevator_calls["down"][i])
                    self.elevator_calls["down"].pop(i)
                    break

    def check_for_new_calls(self) -> None:
        # check for elevator calls.
        # if a elevator was called and the elevator controller did
        # not yet know about this level it adds it to a list of calls.
        for level in self.building.levels:
            if level.up_pressed and level not in self.elevator_calls["up"] and not self.any_elevator_has_level_in_queue(level):
                self.elevator_calls["up"].append(level)
            elif level.down_pressed and level not in self.elevator_calls["down"] and not self.any_elevator_has_level_in_queue(level):
                self.elevator_calls["down"].append(level)

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

    def any_elevator_has_level_in_queue(self, level: Level) -> bool:
        """
        Checks if any elevator is travelling to that level.
        """
        for elevator in self.elevators:
            if level in elevator.queue:
                return True
        return False