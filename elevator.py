class Elevator:
    def __init__(self, capacity: int, speed: float) -> None:
        self.capacity = capacity    # capacity in kg 
        self.speed = speed          # speed of the elevator

        self.level = 0          # tracks the current level of the elevator 
        self.direction = 0      # tracks the direction the elevator is moving 
        self.queue = []         # tracks the target levels
