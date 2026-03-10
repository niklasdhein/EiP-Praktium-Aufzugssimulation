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
