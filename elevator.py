from building import Building

import random

class Elevator:
    def __init__(self, 
    elevator_controller: ElevatorController, 
    capacity: int, 
    speed: float,
    mode: str) -> None:
        self.elevator_controller = elevator_controller  # parent controller
        self.capacity = capacity    # capacity in kg 
        self.speed = speed if self.capacity <= 1000 else speed // 2
        self.mode = mode

        self.width = 100 if self.capacity <= 1000 else 200

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
        def remove_calls_from_level() -> None:
            self.target_level.up_pressed = False
            self.target_level.down_pressed = False

        def smart_remove_controller_call() -> None:
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

        def handle_people_exit() -> None:
            passengers_that_remain = []
            for passenger in self.passengers:
                if self.target_level == passenger.target_level:     # kick out passengers at target
                    passenger.leave_elevator(self.elevator_controller.building.width, self.target_level)
                else:
                    passengers_that_remain.append(passenger)
            self.passengers = passengers_that_remain    # update the passengers

        def handle_people_enter() -> None:
            for passenger in passengers_of_level:
                if passenger.states["elevator_called"] and \
                    not passenger.states["in_elevator"] and \
                    not passenger.states["annoyed"]:
                    passenger.enter_elevator()
                    self.passengers.append(passenger)

        def handle_overweight() -> None:
            while self.get_load() > self.capacity:
                self.passengers[-1].leave_elevator(self.passengers[-1].graphics.x, self.target_level)
                self.passengers.pop()

        def handle_passenger_targets() -> None:
            for passenger in self.passengers:
                if passenger.target_level not in self.queue:
                    self.add_to_queue(passenger.target_level)

        # 1. when the elevator arrives at a level, remove 
        # the call from the level for the elevator
        remove_calls_from_level()

        # 2. if an elevator arrives at a level with a call, but the elevator was not
        # called by this level and holds because he drops people of,
        # then take them in and remove 
        smart_remove_controller_call()

        # 3. get all passengers on the level arrived
        passengers_of_level = self.target_level.passengers

        # 4. drop off all people who want to exit on that level
        # and also update the list of people still in the elevator
        handle_people_exit()

        # 5. from all passengers in the level, let these enter, who have called the elevator
        # and are waiting
        handle_people_enter()

        # 6. check for overweight.
        # when overweight, kick as many people as needed 
        handle_overweight()

        # 7. removes old elevator target, if a target is in queue it
        # gets set as new one.
        self.remove_target()

        # 8. when in algorithm mode respect passenger targets
        # when in random mode just append a new random target to queue
        if self.mode == "algorithm":
            handle_passenger_targets()
        elif self.mode == "random":
            self.add_random_level_to_queue()

    def move(self, dt: float) -> None:
        # print(f"moving by {self.direction * self.speed * dt}")
        self.graphics.y += self.direction * self.speed * dt

    def has_arrived_at_target(self) -> bool:
        return self.direction == 0\
            or self.direction == -1 and self.graphics.y <= self.target_y\
            or self.direction == 1 and self.graphics.y >= self.target_y

    def update(self, dt: float) -> None:
        # only move the elevator if it has a target
        if self.target_level != None:
            # move the elevator a bit each frame
            self.move(dt=dt)

            # check if it has arrived
            if self.has_arrived_at_target():
                self.graphics.y = self.target_y
                self.handle_arrival_at_target()

        # pick a target on your own if algorithm mode is disabled
        # when algorithm mode is enabled targets will get sent by the controller
        # and set by passengers
        elif self.mode != "algorithm":
            if self.mode == "random":
                self.add_random_level_to_queue()
            elif self.mode == "pingpong":
                building_center_y = self.elevator_controller.building.bottom_y -\
                    self.elevator_controller.building.level_count *\
                    self.elevator_controller.building.levels[0].background_gfx.height *\
                    0.5
                if self.graphics.y < building_center_y:
                    self.add_multiple_to_queue(reversed(self.elevator_controller.building.levels))
                else:
                    self.add_multiple_to_queue(self.elevator_controller.building.levels)
            else:
                print("elevator in unknown mode")

    def remove_target(self) -> None:
        """
        A target is removed, when the elevator arrives.
        """
        # remove target from elevator
        self.target_level = None
        self.target_y = None
        self.direction = 0

        self.queue.pop(0)
        if len(self.queue) > 0: 
            self.set_target(self.queue[0])

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

    def add_multiple_to_queue(self, target_levels: [Level]) -> None:
        self.queue += target_levels
        if self.target_level == None and len(self.queue) > 0: # in case some idiot sent empty list and queue was empty
            self.set_target(self.queue[0])

    def add_random_level_to_queue(self) -> None:
        self.add_to_queue(self.elevator_controller.building.levels[random.randint(0, self.elevator_controller.building.level_count-1)])