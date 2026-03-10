class Building:
    level_height = 250
    def __init__(self, levels: int) -> None:
        self.levels = levels
        self.height = self.level_height * self.levels

        self.elevator_controller = None
        self.staircase = None
