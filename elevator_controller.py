import random
import pygame

from elevator import Elevator
from building import Building

class ElevatorController:
    def __init__(self, 
    building: Building, 
    elevator_count: int,
    big_elevator_spawn_probability: float,
    elevator_mode: str,
    use_sprite: bool) -> None:
        self.building = building    # parent building
        self.elevators = []         # children elevators
        self.elevator_mode = elevator_mode

        self.elevator_margin_x = 100
        self.create_random_elevators(elevator_count=elevator_count,
        big_elevator_spawn_probability=big_elevator_spawn_probability,
        elevator_mode=elevator_mode,
        use_sprite=use_sprite)

        # stores all elevator calls from all levels.
        # the calls are seperated in up and down calls for later
        # optimization.
        self.elevator_calls = {
            "up": [],
            "down": []
        }

    def update(self, dt: float, speed_multiplier: float) -> None:
        """
        The controller is the head control-unit of all elevators.
        """
        if self.elevator_mode == "algorithm":
            self.check_for_new_calls()
            self.try_to_send_elevator_to_call()
        self.update_elevators(dt=dt, speed_multiplier=speed_multiplier)

    def update_elevators(self, dt: float, speed_multiplier: float) -> None:
        # call update for every elevator
        for elevator in self.elevators:
            elevator.update(dt=dt, speed_multiplier=speed_multiplier)

    def create_random_elevators(self, 
    elevator_count: int, 
    big_elevator_spawn_probability: float,
    elevator_mode: str,
    use_sprite: bool) -> None:
        """
        Creates random elevators and set these as children of
        the controller.
        """
        offset_x = 0

        # if there is at least one penthouse, create a special elevator for them
        if self.building.levels[-1].level_type == "penthouse":
            # the vip elevator is allowed to access all levels, 
            # except bunker level(s)
            all_levels_without_bunker = []
            for level in self.building.levels:
                if level.level_type != "bunker":
                    all_levels_without_bunker.append(level)

            vip_elevator = Elevator(
                elevator_controller=self,
                speed=120,
                capacity=1000,
                mode=elevator_mode,
                current_level=self.building.ground_level,
                allowed_levels=all_levels_without_bunker,
                use_sprite=use_sprite
            )

            # create a rect for graphics
            vip_elevator.graphics = pygame.Rect(
                offset_x,
                vip_elevator.current_level.background_gfx.y + vip_elevator.current_level.background_gfx.height - 240,
                vip_elevator.width,
                240
            )
            offset_x += vip_elevator.width + self.elevator_margin_x

            # get initial queue for random and pingpong mode
            if elevator_mode == "pingpong":
                vip_elevator.add_to_queue(vip_elevator.allowed_levels[0])
            elif elevator_mode == "random":
                random_level = vip_elevator.allowed_levels[random.randint(0, len(vip_elevator.allowed_levels)-1)]
                vip_elevator.add_to_queue(random_level)

            self.elevators.append(vip_elevator)

        # if there is at least one bunker level, create a special elevator from the lowest
        # basement floor, that is allowed to access the bunker
        if self.building.levels[0].level_type == "bunker":
            # get all bunker levels as well as the last basement level
            bunker_levels_with_last_basement = []
            for level in self.building.levels:
                if level.level_type == "bunker":
                    bunker_levels_with_last_basement.append(level)
                else:
                    bunker_levels_with_last_basement.append(level)
                    break
            
            bunker_elevator = Elevator(
                elevator_controller=self,
                speed=50,
                capacity=2000,
                mode=elevator_mode,
                current_level=bunker_levels_with_last_basement[-1],
                allowed_levels=bunker_levels_with_last_basement,
                use_sprite=use_sprite
            )

            # create a rect for graphics
            bunker_elevator.graphics = pygame.Rect(
                offset_x,
                bunker_elevator.current_level.background_gfx.y + bunker_elevator.current_level.background_gfx.height - 240,
                bunker_elevator.width,
                240
            )
            offset_x += bunker_elevator.width + self.elevator_margin_x

            # get initial queue for random and pingpong mode
            if elevator_mode == "pingpong":
                bunker_elevator.add_to_queue(bunker_elevator.allowed_levels[0])
            elif elevator_mode == "random":
                random_level = bunker_elevator.allowed_levels[random.randint(0, len(bunker_elevator.allowed_levels)-1)]
                bunker_elevator.add_to_queue(random_level)

            self.elevators.append(bunker_elevator)

        # before creating, get all basement and upstairs levels including the ground level
        # since every regualar elevator should be allowed to access these
        for i in range(elevator_count):
            # decide wether big or small elevator
            capacity = 2000 if random.random() <= big_elevator_spawn_probability else 1000

            # instantiate the elevator
            random_elevator = Elevator(elevator_controller=self, 
            speed=100,          # if the speed is too slow and framerate too high the steps get too small for pygame to handle. be careful
            capacity=capacity,
            mode=elevator_mode,
            current_level=self.building.levels[random.randint(0, self.building.level_count-1)],
            allowed_levels=self.building.regular_levels,
            use_sprite=use_sprite
            )
            
            # instantiate the pygame part
            random_elevator.graphics = pygame.Rect(
                offset_x, 
                random_elevator.current_level.background_gfx.y + \
                    random_elevator.current_level.background_gfx.height - 240, 
                random_elevator.width, 
                240)
            offset_x += random_elevator.width + self.elevator_margin_x

            # get initial queue for random and pingpong mode
            if elevator_mode == "pingpong":
                random_elevator.add_to_queue(random_elevator.allowed_levels[0])
            elif elevator_mode == "random":
                random_level = random_elevator.allowed_levels[random.randint(0, len(random_elevator.allowed_levels)-1)]
                random_elevator.add_to_queue(random_level)

            self.elevators.append(random_elevator)

        # for keeping things pretty, center all elevators
        start_x = (self.building.width - self.get_total_elevators_width()) // 2
        for elevator in self.elevators:
            elevator.graphics.x += start_x
            elevator.door = pygame.Rect(
                elevator.graphics.x,
                elevator.graphics.y,
                elevator.graphics.width,
                elevator.graphics.height
            )

    def try_to_send_elevator_to_call(self) -> None:
        """
        An elevator is sent to a call, if it has no elements in its queue.
        """
        for call_up_level in self.elevator_calls["up"]:
            for elevator in self.elevators:
                if len(elevator.queue) == 0 and \
                call_up_level in elevator.allowed_levels and \
                call_up_level != elevator.allowed_levels[-1] and \
                elevator.time_elapsed >= elevator.waittime:
                    elevator.add_to_queue(call_up_level)
                    elevator.target_call = "up"
                    self.elevator_calls["up"].pop(0)
                    break

        for call_down_level in self.elevator_calls["down"]:
            for elevator in self.elevators:
                if len(elevator.queue) == 0 and \
                call_down_level in elevator.allowed_levels and \
                call_down_level != elevator.allowed_levels[0] and \
                elevator.time_elapsed >= elevator.waittime:
                    elevator.add_to_queue(call_down_level)
                    elevator.target_call = "down"
                    self.elevator_calls["down"].pop(0)
                    break

    def check_for_new_calls(self) -> None:
        """
        A call is only registered as new, if it is not already registered
        and no elevator is already moving towards the level. 
        """

        def any_elevator_has_level_in_queue(level) -> bool:
            """
            Checks if any elevator is travelling to that level.
            """
            for elevator in self.elevators:
                if level in elevator.queue:
                    return True
            return False

        def any_elevator_is_moving_towards_level(level) -> bool:
            """
            Checks if any elevator is travelling towards that level right now.
            Returns true if so, false otherwise.
            """
            for elevator in self.elevators:
                if level == elevator.target_level:
                    return True
            return False

        # old version:
        # ignored calls from a level if this level was already in the queue of some
        # elevator
        """for level in self.building.levels:
            if level.up_pressed and level not in self.elevator_calls["up"] and not any_elevator_has_level_in_queue(level):
                self.elevator_calls["up"].append(level)
            elif level.down_pressed and level not in self.elevator_calls["down"] and not any_elevator_has_level_in_queue(level):
                self.elevator_calls["down"].append(level)"""

        # new version:
        # now only ignore calls if the level is the next target of any elevator
        for level in self.building.levels:
            if level.up_pressed and level not in self.elevator_calls["up"] and not any_elevator_is_moving_towards_level(level):
                self.elevator_calls["up"].append(level)
            elif level.down_pressed and level not in self.elevator_calls["down"] and not any_elevator_is_moving_towards_level(level):
                self.elevator_calls["down"].append(level)

    def get_total_elevators_width(self) -> int:
        """
        Calculates the width in px all elevators need and
        returns it.
        """
        width = 0
        for elevator in self.elevators:
            width += elevator.graphics.width
        width += self.elevator_margin_x * (len(self.elevators)-1)
        return width