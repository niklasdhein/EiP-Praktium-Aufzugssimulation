import pygame

class Passenger:
    #states
    waiting = "waiting"
    annoyed = "annoyed"
    in_elevator = "in_elevator"
    using_staircase = "using_staircase"

    def __init__(self, weight: int, target_level: int, patience: int) -> None:
        self.weight = weight                               # weight in kg
        self.target_level = target_level                   # level the passenger wants to travel to
        self.deadline = pygame.time.get_ticks() + patience # time between creation and annoyance
        self.state = self.waiting                          # current state

    #check state
    def update(self) -> None:
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