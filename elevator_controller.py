import random

from elevator import Elevator

class ElevatorController:
    def __init__(self, elevators: [Elevator]) -> None:
        self.elevators = elevators

    def update_elevators(self, dt: float, building: Building) -> None:
        """
        The controller is like the head control-unit of all elevators.
        """
        for elevator in self.elevators:
            if elevator.target_level != None:
                # tells each elevator to move to its target
                elevator.move_to_target(dt=dt)

            else:
                # if an elevator has no target give it a random new one
                elevator.set_target(target_level=random.randint(0, building.levels-1), building=building)