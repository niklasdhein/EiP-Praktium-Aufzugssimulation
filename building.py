class Building:
    level_height = 250
    def __init__(self, levels: int, bottom_y: int) -> None:
        self.levels = levels        # amount of levels the building contains
        self.height = self.level_height * self.levels   # building height in px
        self.bottom_y = bottom_y    # y-coordinate of the bottom edge 

        self.elevator_controller = None     # reference to the elevator controller the building contains
        self.staircase = None               # reference to the staircase the building contains

        self.graphics = []          # Reference to the level graphics