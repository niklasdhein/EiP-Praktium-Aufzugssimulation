import pygame
import random

class Passenger:
    def __init__(self, current_level: Level, target_level: Level, weight: int=120) -> None:
        self.current_level = current_level          # level the passenger is in currently
        self.current_level.passengers.append(self)
        self.target_level = target_level            # level the passenger wants to travel to
        self.weight = weight

        self.walk_target_x = self.current_level.building.elevator_controller.get_total_elevators_width() + 20
        self.walk_speed = 500
        self.walk_direction = -1

        self.states = {
            "elevator_called": False,
            "annoyed": False,
            "in_elevator": False,
            "using_staircase": False,
            "walking": True
        }

        self.graphics = pygame.Rect(
            random.randint(self.current_level.building.width // 2, self.current_level.building.width * 2), 
            self.current_level.building.bottom_y - self.current_level.level * self.current_level.background_gfx.height - 60,
            30, 
            60
            ) 

    def leave_elevator(self) -> None:
        self.states["in_elevator"] = False
        self.states["walking"] = True

        self.graphics.y = self.current_level.background_gfx.y + self.current_level.background_gfx.height - 60
        self.graphics.width = 30
        self.graphics.height = 60

        self.walk_target_x = self.current_level.building.width
        self.walk_direction = 1

    def enter_elevator(self) -> None:
        self.current_level.remove_passenger_from_level(self)

        self.states["elevator_called"] = False
        self.states["in_elevator"] = True

        self.graphics.width = 0
        self.graphics.height = 0

    def move_to_target_x(self, dt: float) -> None:
        """
        Moves the passenger towards its target.
        Does not check if a target is actually set.
        Checks if target is reached.
        """
        self.graphics.x += self.walk_direction * self.walk_speed * dt
        
        # target reached
        if self.walk_direction == -1 and self.graphics.x <= self.walk_target_x\
        or self.walk_direction == 1 and self.graphics.x >= self.walk_target_x:
            self.graphics.x = self.walk_target_x
            self.walk_direction = 0
            self.walk_target_x = None
            
            self.states["walking"] = False

    def update(self, dt: float) -> None:
        """
        Updates the passengers action according to the state he is in.
        """

        # walk to the elevator
        if self.states["walking"]:
            self.move_to_target_x(dt=dt)

        # call elevator
        elif not self.states["elevator_called"] and not self.states["walking"] and not self.states["in_elevator"]:
            self.states["elevator_called"] = True

            # decide wether travel up or down
            if self.target_level.level > self.current_level.level:
                self.current_level.call_elevator_up()
            elif self.target_level.level < self.current_level.level:
                self.current_level.call_elevator_down()