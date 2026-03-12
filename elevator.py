from building import Building

class Elevator:
    def __init__(self, elevator_controller: ElevatorController, capacity: int, speed: float) -> None:
        self.elevator_controller = elevator_controller  # parent controller
        self.capacity = capacity    # capacity in kg 
        self.speed = speed          # speed of the elevator

        if self.capacity > 1150:    # Change the width (px) accordingly to capacity
            self.width = 200
        else:
            self.width = 100

        self.direction = 0          # tracks the direction the elevator is moving 
        self.queue = []             # tracks the target levels
        self.target_level = None    # tracks the level travelling to
        self.target_y = None        # target y coordinate

        self.graphics = None        # stores the pygame object like rect, sprite, ..

        self.passengers = []

    def get_load(self) -> int:
        load = 0
        # iterate over list of passengers
        for i in range(len(self.passengers)):
            load += self.passengers[i].weight

        return load

    def enter_passengers(self, passengers: [Passenger]) -> None:
        for passenger in passengers:
            if passenger.states["elevator_called"]:
                passenger.states["in_elevator"] = True
                self.passengers.append(passenger)

    def handle_arrival_at_target(self) -> None:
        # remove the call from the level
        self.target_level.up_pressed = False
        self.target_level.down_pressed = False

        # load in passengers
        self.enter_passengers(self.target_level.passengers)

        # stop elevator from moving
        self.remove_target()

    def move_to_target(self, dt: float) -> None:
        """
        Moves the elevator to the target level.
        In order to move smoothly and correctly it needs the deltatime calculated
        by pygame in the game loop.
        """
        # move the elevator a bit each frame
        self.graphics.y += self.direction * self.speed * dt

        # check if it has arrived
        if self.direction == 0\
        or self.direction == -1 and self.graphics.y <= self.target_y\
        or self.direction == 1 and self.graphics.y >= self.target_y:
            self.graphics.y = self.target_y # prevent clipping
            self.handle_arrival_at_target()            

    def remove_target(self) -> None:
        """
        A target is removed, when the elevator arrives.
        """
        # remove target from elevator
        self.target_level = None
        self.target_y = None
        self.direction = 0
        self.queue.pop(0)

    def set_target(self, target_level: Level) -> None:
        """
        Calculates the target y postion and sets the target level
        the elevator should travel to.
        To do that correctly it needs information about the height of
        each level as well as the window height, since the building is
        drawn bottom to top.
        """
        target_y = target_level.graphics.y + target_level.graphics.height - self.graphics.height

        self.target_level = target_level
        self.target_y = target_y
        if self.graphics.y < self.target_y: self.direction = 1
        elif self.graphics.y > self.target_y: self.direction = -1
        else: self.direction = 0

    def add_to_queue(self, target_level: Level) -> None:
        self.queue.append(target_level)
        if self.target_level == None:
            self.set_target(self.queue[0])