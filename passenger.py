import pygame
import random

class Passenger:
    def __init__(self, 
    current_level: Level, 
    target_level: Level,
    patience: int,  
    weight: int, 
    walk_speed: int) -> None:
        self.current_level = current_level          # level the passenger is in currently
        self.target_level = target_level            # level the passenger wants to travel to
        self.patience = patience
        self.weight = weight
        self.walk_speed = walk_speed
        
        self.current_patience = self.patience
        self.walk_target_x = None
        self.walk_direction = 0

        self.states = {
            "elevator_called": False,
            "annoyed": False,
            "in_elevator": False,
            "using_staircase": False,
            "walking": False
        }

        self.current_level.passengers.append(self)

        self.graphics = pygame.Rect(
            -30 if random.random() <= 0.5 else self.current_level.building.width, 
            self.current_level.background_gfx.y + self.current_level.background_gfx.height - 60,
            30, 
            60
            ) 

        # spawn each passenger with target to walk towards elevators
        screen_center_x = self.current_level.building.width // 2
        half_total_elevators_width = self.current_level.building.elevator_controller.get_total_elevators_width() // 2
        target_x = random.randint(screen_center_x - half_total_elevators_width, screen_center_x + half_total_elevators_width)
        self.set_target(target_x=target_x)

    def leave_elevator(self, target_x: int, new_level: Level) -> None:
        self.states["in_elevator"] = False
        self.states["elevator_called"] = False
        self.current_level = new_level
        new_level.passengers.append(self)
        self.graphics.y = self.current_level.background_gfx.y + self.current_level.background_gfx.height - 60
        self.graphics.width = 30
        self.graphics.height = 60

        self.set_target(target_x=target_x)

    def enter_elevator(self, target_x: int, direction: int) -> bool:
        # do not enter, when the elevator is moving in a direction you do not want to go to
        if direction == 1 and self.target_level.level > self.current_level.level\
            or direction == -1 and self.target_level.level < self.current_level.level:
            return False

        # only enter either if the elevator has no direction, so it will respect yours
        # or if it has the same direction as you
        self.current_level.remove_passenger_from_level(self)

        self.states["elevator_called"] = False
        self.states["in_elevator"] = True

        self.set_target(target_x=target_x)
        return True

    def move_to_target_x(self, dt: float, speed_multiplier: float) -> None:
        """
        Moves the passenger towards its target.
        Does not check if a target is actually set.
        Checks if target is reached.
        """
        self.graphics.x += self.walk_direction * self.walk_speed * speed_multiplier * dt
        
        # target reached
        if self.walk_direction == -1 and self.graphics.x <= self.walk_target_x\
        or self.walk_direction == 1 and self.graphics.x >= self.walk_target_x:
            self.remove_target()
            if self.states["in_elevator"]:
                self.graphics.width = 0
                self.graphics.height = 0

    def remove_target(self) -> None:
        self.graphics.x = self.walk_target_x
        self.walk_direction = 0
        self.walk_target_x = None
        self.states["walking"] = False

    def set_target(self, target_x: int) -> None:
        self.walk_target_x = target_x
        self.states["walking"] = True

        if self.walk_target_x > self.graphics.x: self.walk_direction = 1
        elif self.walk_target_x < self.graphics.x: self.walk_direction = -1
        else: self.remove_target()

    def update(self, dt: float, speed_multiplier: float) -> None:
        """
        Updates the passengers action according to the state he is in.
        """

        # walk to the elevator
        if self.states["walking"]:
            self.move_to_target_x(dt=dt, speed_multiplier=speed_multiplier)

        # call elevator
        elif not self.states["elevator_called"] and\
            not self.states["in_elevator"] and\
            self.current_level != self.target_level:
            self.states["elevator_called"] = True

            # decide wether travel up or down
            if self.target_level.level > self.current_level.level:
                self.current_level.call_elevator_up()
            elif self.target_level.level < self.current_level.level:
                self.current_level.call_elevator_down()

        # check if lost patience
        elif self.states["elevator_called"] and\
            not self.states["in_elevator"] and\
            self.current_level != self.target_level:
            self.current_patience -= dt * speed_multiplier
            if self.current_patience <= 0 and not self.states["annoyed"]:
                self.states["annoyed"] = True
                self.set_target(self.current_level.building.width)
                self.current_level.passengers_annoyed += 1