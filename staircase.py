class Staircase:
    def __init__(self, capacity: int, speed: int):
        self.capacity = capacity
        self.speed = speed
        self.passengers = []
        if len(self.passengers) >= self.capacity:
            self.speed = self.speed//2

    def use_stairs(self, passenger) -> None:
        self.passenger.append(passenger)
