import random

from passenger import Passenger

class Codsworth(Passenger):
    def __init__(
        self,
        current_level: Level, 
        target_level: Level,
        bunker_elevator_level: Level,
        patience: int,  
        weight: int, 
        walk_speed: int,
        use_sprite: bool
    ) -> None:
        super().__init__(
            current_level=current_level,
            target_level=target_level,
            patience=patience,
            weight=weight,
            walk_speed=walk_speed,
            use_sprite=use_sprite
        )

        # set the bunker elevator as first target, also remember
        # the actual bunker level
        self.bunker_elevator_level = bunker_elevator_level
        self.bunker_target_level = self.target_level
        self.target_level = self.bunker_elevator_level

    def leave_elevator(self, target_x: int, new_level: Level) -> None:
        self.states["in_elevator"] = False
        self.states["elevator_called"] = False
        self.current_level = new_level
        new_level.passengers.append(self)
        self.graphics.y = self.current_level.background_gfx.y + self.current_level.background_gfx.height - 60
        self.visible = True
        self.set_target(target_x=target_x)

        if self.current_level == self.bunker_elevator_level:
            # update the new target to the bunker level
            self.target_level = self.bunker_target_level

            # tell the passenger to walk towards an elevator again
            screen_center_x = self.current_level.building.width // 2
            half_total_elevators_width = self.current_level.building.elevator_controller.get_total_elevators_width() // 2
            target_x = random.randint(screen_center_x - half_total_elevators_width, screen_center_x + half_total_elevators_width)
            self.set_target(target_x=target_x)
