class VIP(passenger):
    def __init__(
    self,
    current_level: Level, 
    target_level: Level,
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
        