import pygame
import random

class Passenger:
    def __init__(self, building: Building, target_level: int=0, weight: int=80 , patience: int=0) -> None:
        self.building = building
        self.travel_target_level = target_level    # level the passenger wants to travel to
        self.current_level = random.randint(0, self.building.level_count-1)

        self.walk_target_x = building.elevator_controller.get_total_elevators_width() + 20
        self.walk_speed = 500
        self.walk_direction = -1

        self.states = {
            "waiting": False,
            "elevator_called": False,
            "annoyed": False,
            "in_elevator": False,
            "using_staircase": False,
            "walking": True,
            "travel_target_level_reached": False
        }

        # self.weight = weight                      # weight in kg
        # self.deadline = pygame.time.get_ticks() + patience # time between creation and annoyance
        # self.state = self.waiting                          # current state

        # visuals
        self.graphics = pygame.Rect(random.randint(self.building.width // 2, self.building.width * 2), self.building.bottom_y - \
            self.current_level * self.building.levels[0].height - 60, 30, 60)

    def move_to_target_x(self, dt: float) -> None:
        self.graphics.x += self.walk_direction * self.walk_speed * dt
        
        # target reached
        if self.walk_direction == -1 and self.graphics.x <= self.walk_target_x:
            self.graphics.x = self.walk_target_x
            self.walk_direction = 0
            self.walk_target_x = None
            
            self.states["walking"] = False
            self.states["waiting"] = True


    #check state
    def update(self, dt: float) -> None:
        # walk to the elevator
        if self.states["walking"]:
            self.move_to_target_x(dt=dt)

        # call elevator
        elif self.states["waiting"] and not self.states["elevator_called"]:
            self.states["elevator_called"] = True
            self.building.elevator_controller.call_elevator(to_level=self.current_level)

        """
        if self.state == self.waiting:
            time = pygame.time.get_ticks()
            if time >= self.deadline:
                self.state = self.annoyed

        elif self.state == self.annoyed:
            #zum Treppenhaus laufen
            pass

        elif self.state == self.in_elevator:
            pass

        elif self.state == self.using_staircase:
            pass

        elif self.state == self.walking:
            pass

        elif self.state == self.target_reached:
            pass
        """