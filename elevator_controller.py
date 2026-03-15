import random
import pygame

from elevator import Elevator
from building import Building

class ElevatorController:
    def __init__(self, 
    building: Building, 
    elevator_count: int,
    big_elevator_spawn_probability: float,
    elevator_mode: str) -> None:
        self.building = building    # parent building
        self.elevators = []         # children elevators
        self.elevator_mode = elevator_mode

        self.elevator_margin_x = 100
        self.create_random_elevators(elevator_count=elevator_count,
        big_elevator_spawn_probability=big_elevator_spawn_probability,
        elevator_mode=elevator_mode)

        # stores all elevator calls from all levels.
        # the calls are seperated in up and down calls for later
        # optimization.
        self.elevator_calls = {
            "up": [],
            "down": []
        }

    def update(self, dt: float, speed_multiplier: float) -> None:
        """
        The controller is like the head control-unit of all elevators.
        """

        if self.elevator_mode == "algorithm":
            self.check_for_new_calls()
            self.try_to_send_elevator_to_call()
        self.update_elevators(dt=dt, speed_multiplier=speed_multiplier)

    def update_elevators(self, dt: float, speed_multiplier: float) -> None:
        # call update for every elevator
        for elevator in self.elevators:
            elevator.update(dt=dt, speed_multiplier=speed_multiplier)

    def create_random_elevators(self, 
    elevator_count: int, 
    big_elevator_spawn_probability: float,
    elevator_mode: str) -> None:
        """
        Creates random elevators and set these as children of
        the controller.
        """
        offset_x = 0
        for i in range(elevator_count):
            # decide wether big or small elevator
            capacity = 2000 if random.random() <= big_elevator_spawn_probability else 1000

            # instantiate the elevator
            random_elevator = Elevator(elevator_controller=self, 
            speed=100,          # if the speed is too slow and framerate too high the steps get too small for pygame to handle. be careful
            capacity=capacity,
            mode=elevator_mode,
            current_level=self.building.levels[random.randint(0, self.building.level_count-1)]
            )
            
            # instantiate the pygame part
            random_elevator.graphics = pygame.Rect(
                offset_x, 
                self.building.bottom_y - random_elevator.current_level.background_gfx.height\
                * random_elevator.current_level.level - 200, 
                random_elevator.width, 
                200)
            offset_x += random_elevator.width + self.elevator_margin_x

            self.elevators.append(random_elevator)

        # for keeping things pretty, center all elevators
        start_x = (self.building.width - self.get_total_elevators_width()) // 2
        for elevator in self.elevators:
            elevator.graphics.x += start_x

    def try_to_send_elevator_to_call(self) -> None:
        # handle which elevator travels to which floor
        for call_up_level in self.elevator_calls["up"]:
            for elevator in self.elevators:
                if len(elevator.queue) == 0:
                    elevator.add_to_queue(call_up_level)
                    self.elevator_calls["up"].pop(0)
                    break

        for call_down_level in self.elevator_calls["down"]:
            for elevator in self.elevators:
                if len(elevator.queue) == 0:
                    elevator.add_to_queue(call_down_level)
                    self.elevator_calls["down"].pop(0)
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

    def get_total_elevators_width(self) -> int:
        """
        Calculates the width in px all elevators need and
        returns it.
        """
        width = 0
        for elevator in self.elevators:
            width += elevator.graphics.width
        width += self.elevator_margin_x * (len(self.elevators)-1)
        return width

    def any_elevator_has_level_in_queue(self, level: Level) -> bool:
        """
        Checks if any elevator is travelling to that level.
        """
        for elevator in self.elevators:
            if level in elevator.queue:
                return True
        return False