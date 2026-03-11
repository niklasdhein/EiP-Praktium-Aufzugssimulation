from building import Building

class Elevator:
    height = 200
    def __init__(self, elevator_controller: ElevatorController, capacity: int, speed: float) -> None:
        self.elevator_controller = elevator_controller  # parent controller
        self.capacity = capacity    # capacity in kg 
        self.speed = speed          # speed of the elevator

        if self.capacity > 1150:    # Change the width (px) accordingly to capacity
            self.width = 200
        else:
            self.width = 100

        self.level = 0              # tracks the current level of the elevator 
        self.direction = 0          # tracks the direction the elevator is moving 
        self.queue = []             # tracks the target levels
        self.target_level = None    # tracks the level travelling to
        self.target_y = None        # tracks target y coordinate

        self.graphics = None        # stores the pygame object like rect, sprite, ..

        self.passengers = []

    def get_load(self) -> int:
        load = 0
        # iterate over list of passengers
        for i in range(len(self.passengers)):
            load += self.passengers[i].weight

        return load

    # passenger enters elevator
    def enter(self, passenger) -> None:
        self.passengers.append(passenger)
        # check if overloaded
        if self.get_load() > self.capacity:
            self.passengers.pop()
            return
        # add target_level to queue
        elif passenger.target_level not in self.queue:
            self.queue.append(passenger.target_level)
        # passenger is in elevator
        passenger.state = passenger.in_elevator

    def move_to_target(self, dt: float) -> None:
        """
        Moves the elevator to the target level.
        In order to move smoothly and correctly it needs the deltatime calculated
        by pygame in the game loop.
        """
        # move the elevator a bit each frame
        self.graphics.y += self.direction * self.speed * dt

        self.level = (self.elevator_controller.building.bottom_y - self.graphics.y) //\
            self.elevator_controller.building.levels[0].height

        # check if it has arrived
        if self.direction == -1 and self.graphics.y <= self.target_y\
        or self.direction == 1 and self.graphics.y >= self.target_y:
            self.graphics.y = self.target_y
            self.remove_target()

    def remove_target(self) -> None:
        """
        Little function, that just clears up variables used to manage travelling
        to save resources.
        """
        self.target_level = None
        self.target_y = None
        self.direction = 0

    def set_target(self, target_level: int) -> None:
        """
        Calculates the target y postion and sets the target level
        the elevator should travel to.
        To do that correctly it needs information about the height of
        each level as well as the window height, since the building is
        drawn bottom to top.
        """
        building = self.elevator_controller.building

        print("target level: " + str(target_level))

        # calculate target y position
        target_y = building.levels[target_level].graphics.y + building.levels[target_level].height - self.height

        # return if elevator is already at exactly this positon
        if target_y == self.graphics.y: return

        self.target_level = target_level
        self.target_y = target_y
        if self.graphics.y < self.target_y: self.direction = 1
        elif self.graphics.y > self.target_y: self.direction = -1