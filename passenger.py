import pygame
import random

class Passenger:
    def __init__(self, 
    current_level, 
    target_level,
    patience: int,  
    weight: int, 
    walk_speed: int,
    use_sprite: bool,
    entity_scale_factor: float) -> None:
        self.current_level = current_level          # level the passenger is in currently
        self.target_level = target_level            # level the passenger wants to travel to
        self.patience = patience
        self.weight = weight
        self.walk_speed = walk_speed
        self.entity_scale_factor = entity_scale_factor

        self.use_sprite = use_sprite
        self.shown_surface_index = 0
        self.frametime = 0

        self.left_loaded_surfaces = []
        self.right_loaded_surfaces = []
        self.good_left_loaded_surfaces = []
        self.good_right_loaded_surfaces = []
        self.bad_right_loaded_surfaces = []
        self.idle_loaded_surfaces = []

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

        self.visible = True

        self.current_level.passengers.append(self)

        # load sprites from disk
        if self.use_sprite:
            image_directory = "./sprites/"
            left_image_files = [
                "walk_left_1.png",
                "walk_left_2.png",
                "walk_left_3.png",
                "walk_left_4.png",
                "walk_left_5.png",
                "walk_left_6.png"
            ]
            right_image_files = [
                "walk_right_1.png",
                "walk_right_2.png",
                "walk_right_3.png",
                "walk_right_4.png",
                "walk_right_5.png",
                "walk_right_6.png"
            ]
            good_left_image_files = [
                "good_walk_left_1.png",
                "good_walk_left_2.png",
                "good_walk_left_3.png",
                "good_walk_left_4.png",
                "good_walk_left_5.png",
                "good_walk_left_6.png"
            ]
            good_right_files = [
                "good_walk_right_1.png",
                "good_walk_right_2.png",
                "good_walk_right_3.png",
                "good_walk_right_4.png",
                "good_walk_right_5.png",
                "good_walk_right_6.png"
            ]
            bad_right_files = [
                "bad_walk_right_1.png",
                "bad_walk_right_2.png",
                "bad_walk_right_3.png",
                "bad_walk_right_4.png",
                "bad_walk_right_5.png",
                "bad_walk_right_6.png",
            ]
            idle_image_files = [
                "idle_1.png",
                "idle_2.png",
                "idle_3.png",
                "idle_4.png",
                "idle_5.png",
                "idle_6.png",
                "idle_7.png",
                "idle_8.png",
                "idle_9.png",
                "idle_10.png"
            ]

            for image in left_image_files:
                left_loaded_surface = pygame.image.load(image_directory + image)
                left_loaded_surface = left_loaded_surface.convert_alpha()
                left_loaded_surface = pygame.transform.scale(left_loaded_surface, (60 * self.entity_scale_factor, 60 * self.entity_scale_factor))

                self.left_loaded_surfaces.append(left_loaded_surface)

            for image in right_image_files:
                right_loaded_surface = pygame.image.load(image_directory + image)
                right_loaded_surface = right_loaded_surface.convert_alpha()
                right_loaded_surface = pygame.transform.scale(right_loaded_surface, (60 * self.entity_scale_factor, 60 * self.entity_scale_factor))

                self.right_loaded_surfaces.append(right_loaded_surface)

            for image in good_left_image_files:
                good_left_loaded_surface = pygame.image.load(image_directory + image)
                good_left_loaded_surface = good_left_loaded_surface.convert_alpha()
                good_left_loaded_surface = pygame.transform.scale(good_left_loaded_surface, (60 * self.entity_scale_factor, 60 * entity_scale_factor))

                self.good_left_loaded_surfaces.append(good_left_loaded_surface)

            for image in good_right_files:
                good_right_loaded_surface = pygame.image.load(image_directory + image)
                good_right_loaded_surface = good_right_loaded_surface.convert_alpha()
                good_right_loaded_surface = pygame.transform.scale(good_right_loaded_surface, (60 * self.entity_scale_factor, 60 * self.entity_scale_factor))

                self.good_right_loaded_surfaces.append(good_right_loaded_surface)

            for image in bad_right_files:
                bad_right_loaded_surface = pygame.image.load(image_directory + image)
                bad_right_loaded_surface = bad_right_loaded_surface.convert_alpha()
                bad_right_loaded_surface = pygame.transform.scale(bad_right_loaded_surface, (60 * self.entity_scale_factor, 60 * self.entity_scale_factor))

                self.bad_right_loaded_surfaces.append(bad_right_loaded_surface)

            for image in idle_image_files:
                idle_loaded_surface = pygame.image.load(image_directory + image)
                idle_loaded_surface = idle_loaded_surface.convert_alpha()
                idle_loaded_surface = pygame.transform.scale(idle_loaded_surface, (60 * self.entity_scale_factor, 60 * self.entity_scale_factor))

                self.idle_loaded_surfaces.append(idle_loaded_surface)

        self.graphics = pygame.Rect(
            -60 * self.entity_scale_factor if random.random() <= 0.5 else self.current_level.building.width, 
            self.current_level.background_gfx.y + self.current_level.background_gfx.height - 60 * self.entity_scale_factor,
            60 * self.entity_scale_factor, 
            60 * self.entity_scale_factor
        ) 

        # spawn each passenger with target to walk towards elevators
        screen_center_x = self.current_level.building.width // 2
        half_total_elevators_width = self.current_level.building.elevator_controller.get_total_elevators_width() // 2
        target_x = random.randint(screen_center_x - half_total_elevators_width, screen_center_x + half_total_elevators_width)
        self.set_target(target_x=target_x)

    def leave_elevator(self, target_x: int, new_level) -> None:
        self.states["in_elevator"] = False
        self.states["elevator_called"] = False
        self.current_level = new_level
        new_level.passengers.append(self)
        self.graphics.y = self.current_level.background_gfx.y + self.current_level.background_gfx.height - 60 * self.entity_scale_factor
        self.visible = True

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
                self.visible = False

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

        # reset animation each time the target changes
        self.shown_surface_index = 0

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

        # change to next frame
        if self.frametime >= 0.2:
            if self.walk_direction != 0:
                self.shown_surface_index = (self.shown_surface_index + 1) % 6
            else:
                self.shown_surface_index = (self.shown_surface_index + 1) % 10
            self.frametime = 0

        # update the time the current frame is shown
        self.frametime += dt * speed_multiplier