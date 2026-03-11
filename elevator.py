class Elevator:
    height = 200
    def __init__(self, capacity: int, speed: float) -> None:
        self.capacity = capacity    # capacity in kg 
        self.speed = speed          # speed of the elevator

        if self.capacity > 1150:    # Change the width accordingly to capacity
            self.width = 200
        else:
            self.width = 100

        self.level = 0              # tracks the current level of the elevator 
        self.direction = 0          # tracks the direction the elevator is moving 
        self.queue = []             # tracks the target levels
        self.target_level = None    # tracks the level travelling to
        self.target_y = None        # tracks target y coordinate

        self.graphics = None        # stores the pygame object like rect, sprite, ..

    def move_to_target_level(self, dt: float) -> None:
        """
        Moves the elevator to the target level.
        In order to move smoothly and correctly it needs the deltatime calculated
        by pygame in the game loop.
        It also needs the height of the levels in the building to calculate
        the correct target coordinate.
        """
        # return if no target is set to save resources
        if not self.target_level: return

        # move the elevator a bit each frame
        self.graphics.y += self.direction * self.speed * dt

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

    def set_target(self, target_level: int, building: Building) -> None:
        """
        Calculates the target y postion and sets the target level
        the elevator should travel to.
        To do that correctly it needs information about the height of
        each level as well as the window height, since the building is
        drawn bottom to top.
        """
        self.target_level = target_level
        self.target_y = building.bottom_y - target_level * building.level_height - self.height
        if self.graphics.y < self.target_y: self.direction = 1
        elif self.graphics.y > self.target_y: self.direction = -1
        else: self.direction = 0