from passenger import Passenger

class Elevator:
    height = 200
    def __init__(self, capacity: int, speed: float) -> None:
        self.capacity = capacity    # capacity in kg 
        self.speed = speed          # speed of the elevator

        if self.capacity > 1150:    # Change the width accordingly to capacity
            self.width = 200
        else:
            self.width = 100

        self.level = 0          # tracks the current level of the elevator 
        self.direction = 0      # tracks the direction the elevator is moving 
        self.queue = []         # tracks the target levels
        self.passengers = []    # tracks the passengers

    def get_load(self) -> int:
        load = 0

        for i in range(len(self.passengers)):
            load += self.passengers[i].weight

        return load

    # passenger enters elevator
    def enter(self, passenger) -> None:
        self.passengers.append(passenger)
        # check if overloaded
        if self.get_load() > self.capacity:
            self.passengers.pop()

        if passenger.target_level not in self.queue:
            self.queue.append(passenger.target_level)