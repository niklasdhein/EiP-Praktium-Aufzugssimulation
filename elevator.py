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

    def handle_arrival_at_target(self) -> None:
        # 1. when the elevator arrives at a level, remove 
        # the call from the level for the elevator
        self.target_level.up_pressed = False
        self.target_level.down_pressed = False

        # 2. if an elevator arrives at a level with a call, but the elevator was not
        # called by this level and holds because he drops people of,
        # then take them in and remove 
        if self.target_level in self.elevator_controller.elevator_calls["up"]:
            new_calls_up = []
            for call_level in self.elevator_controller.elevator_calls["up"]:
                if call_level != self.target_level:
                    new_calls_up.append(call_level)
            self.elevator_controller.elevator_calls["up"] = new_calls_up
        if self.target_level in self.elevator_controller.elevator_calls["down"]:
            new_calls_down = []
            for call_level in self.elevator_controller.elevator_calls["down"]:
                if call_level != self.target_level:
                    new_calls_down.append(call_level)
            self.elevator_controller.elevator_calls["down"] = new_calls_down

        # 3. get all passengers on the level arrived
        passengers_of_level = self.target_level.passengers

        # 4. drop off all people who want to exit on that level
        # and also update the list of people still in the elevator
        passengers_that_remain = []
        for passenger in self.passengers:
            if self.target_level == passenger.target_level:     # kick out passengers at target
                passenger.leave_elevator(self.elevator_controller.building.width, self.target_level)
            else:
                passengers_that_remain.append(passenger)
        self.passengers = passengers_that_remain    # update the passengers

        # 5. from all passengers in the level, let these enter, who have called the elevator
        # and are waiting
        for passenger in passengers_of_level:
            if passenger.states["elevator_called"]:
                passenger.enter_elevator()
                self.passengers.append(passenger)

        print(f"all people handled. weight: {self.get_load()}")

        # 6. check for overweight.
        # when overweight, kick as many people as needed 
        while self.get_load() > self.capacity:
            self.passengers[-1].leave_elevator(self.passengers[-1].graphics.x, self.target_level)
            self.passengers.pop()
            print(f"OVERWEIGHT! kicked last person. weight: {self.get_load()} / {self.capacity}")

        # 7. remove the old target from the elevator.
        # if something is still in queue, set this as new target
        self.remove_target()

        # 8. add all target levels from the passengers to the queue
        for passenger in self.passengers:
            if passenger.target_level not in self.queue:
                self.add_to_queue(passenger.target_level)

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
        if len(self.queue) > 0: self.set_target(self.queue[0])

    def set_target(self, target_level: Level) -> None:
        target_y = target_level.background_gfx.y + target_level.background_gfx.height - self.graphics.height

        self.target_level = target_level
        self.target_y = target_y
        if self.graphics.y < self.target_y: self.direction = 1
        elif self.graphics.y > self.target_y: self.direction = -1
        else: self.direction = 0

    def add_to_queue(self, target_level: Level) -> None:
        self.queue.append(target_level)
        if self.target_level == None:
            self.set_target(self.queue[0])