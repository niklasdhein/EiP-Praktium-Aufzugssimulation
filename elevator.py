from building import Building

import random

class Elevator:
    def __init__(self, 
    elevator_controller: ElevatorController, 
    capacity: int, 
    speed: float,
    mode: str,
    current_level: Level,
    allowed_levels: [Level]) -> None:
        self.elevator_controller = elevator_controller  # parent controller
        self.capacity = capacity    # capacity in kg 
        self.speed = speed if self.capacity <= 1000 else speed * 0.75
        self.mode = mode
        self.current_level = current_level
        self.allowed_levels = allowed_levels

        self.width = 100 if self.capacity <= 1000 else 200

        self.direction = 0          # tracks the direction the elevator is moving 
        self.queue = []             # tracks the target levels
        self.target_level = None    # tracks the level travelling to
        self.target_y = None        # target y coordinate
        self.target_call = None

        self.waittime = 8           # seconds of doors opened
        self.time_elapsed = 0
        self.handled_exit_from_target = False

        self.graphics = None        # stores the pygame object like rect, sprite, ..
        self.door = None

        self.passengers = [] 

        # statistic variables
        self.passengers_transported = 0

    def get_load(self) -> int:
        load = 0
        # iterate over list of passengers
        for i in range(len(self.passengers)):
            load += self.passengers[i].weight

        return load

    def remove_call_from_level(self) -> None:
        if self.target_call == "up" or self.direction == -1:
            self.current_level.up_pressed = False
        elif self.target_call == "down" or self.direction == 1:
            self.current_level.down_pressed = False
   
    def smart_remove_controller_call(self) -> None:
        if self.current_level in self.elevator_controller.elevator_calls["up"]:
            new_calls_up = []
            for call_level in self.elevator_controller.elevator_calls["up"]:
                if call_level != self.current_level:
                    new_calls_up.append(call_level)
            self.elevator_controller.elevator_calls["up"] = new_calls_up
        if self.current_level in self.elevator_controller.elevator_calls["down"]:
            new_calls_down = []
            for call_level in self.elevator_controller.elevator_calls["down"]:
                if call_level != self.current_level:
                    new_calls_down.append(call_level)
            self.elevator_controller.elevator_calls["down"] = new_calls_down

    def move(self, dt: float, speed_multiplier: float) -> None:
        delta = self.direction * self.speed * speed_multiplier * dt
        self.graphics.y += delta
        self.door.y += delta

    def has_arrived_at_target(self) -> bool:
        # returns true if either was moving and reached the target or
        # is not moving but already is at target
        return self.direction == -1 and self.graphics.y <= self.target_y\
            or self.direction == 1 and self.graphics.y >= self.target_y\
            or self.direction == 0 and self.graphics.y == self.target_y

    def update(self, dt: float, speed_multiplier: float) -> None:
        def handle_arrival_at_target() -> None:
            def handle_people_exit() -> None:
                passengers_that_remain = []
                for passenger in self.passengers:
                    if self.current_level == passenger.target_level:     # kick out passengers at target
                        building_width = self.elevator_controller.building.width
                        passenger.leave_elevator(-60 if random.random() <= 0.5 else building_width, self.target_level)
                        self.passengers_transported += 1
                    else:
                        passengers_that_remain.append(passenger)
                self.passengers = passengers_that_remain    # update the passengers
            # 1. sets current level to the reached target
            self.current_level = self.target_level

            # 2. drop off all people who want to exit on that level
            # and also update the list of people still in the elevator
            handle_people_exit()

            # 3. removes old elevator target
            self.remove_target()

            # 4. get the next target from queue (only algorithm mode)
            if self.mode == "algorithm":
                if len(self.queue) > 0:
                    self.set_target(self.queue[0])
            
            # set a random target when in random mode
            elif self.mode == "random":
                level_count = self.elevator_controller.building.level_count
                random_level = self.elevator_controller.building.levels[random.randint(0, level_count-1)]
                self.add_to_queue(random_level)
            
            elif self.mode == "pingpong":
                all_levels = self.elevator_controller.building.levels
                if self.current_level == all_levels[-1]:
                    self.add_multiple_to_queue(reversed(all_levels[:-1]))
                elif self.current_level == all_levels[0]:
                    self.add_multiple_to_queue(all_levels[1:])
                else:
                    self.set_target(self.queue[0])

            # 5. when the elevator arrives at a level, remove 
            # the call from the level for the elevator
            self.remove_call_from_level()

            # 6. if an elevator arrives at a level with a call, but the elevator was not
            # called by this level and holds because he drops people of,
            # then take them in and remove 
            self.smart_remove_controller_call()

            # 7. reset call
            self.target_call = None

        def handle_overweight() -> None:
            while self.get_load() > self.capacity:
                self.passengers[-1].leave_elevator(self.passengers[-1].graphics.x, self.current_level)
                self.passengers.pop()

        def add_calls_on_the_way() -> None:
            # check down calls
            if self.direction == 1:
                passing_levels = self.elevator_controller.building.levels[self.current_level.level-1:self.target_level.level:-1]
                for level in passing_levels:
                    if level in self.elevator_controller.elevator_calls["down"]:
                        self.add_as_first_to_queue(target_level=level)

            # check up calls
            elif self.direction == -1:
                passing_levels = self.elevator_controller.building.levels[self.current_level.level+1:self.target_level.level]
                for level in passing_levels:
                    if level in self.elevator_controller.elevator_calls["up"]:
                        self.add_as_first_to_queue(target_level=level)

        # == move if allowed to ==
        if self.time_elapsed >= self.waittime:

            self.move(dt=dt, speed_multiplier=speed_multiplier)

            # check if the exit has not been handled yet
            if not self.handled_exit_from_target:
                self.remove_call_from_level()           # before leaving
                self.smart_remove_controller_call()     # remove all calls
                handle_overweight()                     # also handle overweight
                add_calls_on_the_way()
                self.handled_exit_from_target = True

            # check if arrival has not been handled yet
            elif self.has_arrived_at_target():
                self.graphics.y = self.target_y
                self.door.y = self.target_y
                handle_arrival_at_target()
                self.time_elapsed = 0
                self.handled_exit_from_target = False

            # if doors are not closed fully, close them
            if self.door.width > 0:
                self.door.width -= dt * speed_multiplier * 200
                if self.door.width < 0:
                    self.door.width = 0
        
        # == else wait for passengers and get their targets (only in algorithm mode) ==
        else:
            passengers_of_level = self.current_level.passengers
            for passenger in passengers_of_level:
                # only let these passengers in the level enter who
                # have called the elevator, are not annoyed, are
                # not already in the elevator and want to travel to a level
                # the elevator is actually allowed to travel to
                if passenger.states["elevator_called"] and \
                    not passenger.states["in_elevator"] and \
                    not passenger.states["annoyed"] and \
                    passenger.target_level in self.allowed_levels and \
                    passenger.enter_elevator(target_x=self.graphics.x+self.graphics.width//2, direction=self.direction):
                        if not passenger.target_level in self.queue and self.mode == "algorithm":
                            self.add_to_queue(passenger.target_level)
                        self.passengers.append(passenger)
                    

            # if doors are not opened, open them
            if self.door.width < self.graphics.width:
                self.door.width += dt * speed_multiplier * 200
                if self.door.width > self.graphics.width:
                    self.door.width = self.graphics.width
        
        # count up the time elapsed since last arrival
        self.time_elapsed += dt * speed_multiplier
        
    def remove_target(self) -> None:
        """
        A target is removed, when the elevator arrives.
        """
        # resets current target and deletes it from the queue
        self.target_level = None
        self.target_y = None
        self.direction = 0
        self.queue.pop(0)

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

    def add_as_first_to_queue(self, target_level: Level) -> None:
        # get the new queue without this target level, if it was in it, since it now gets moved
        # to the first position. this avoids double levels
        new_queue = []
        for q in self.queue:
            if q != target_level: 
                new_queue.append(q)

        self.queue = [target_level] + new_queue
        self.set_target(self.queue[0])

    def add_multiple_to_queue(self, target_levels: [Level]) -> None:
        self.queue += target_levels
        if self.target_level == None and len(self.queue) > 0: # in case some idiot sent empty list and queue was empty
            self.set_target(self.queue[0])

    def add_random_level_to_queue(self) -> None:
        self.add_to_queue(self.elevator_controller.building.levels[random.randint(0, self.elevator_controller.building.level_count-1)])