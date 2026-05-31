from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameSettings:
    screen_width: int = 900
    screen_height: int = 700
    fps: int = 60
    player_size: tuple[int, int] = (60, 48)
    enemy_size: tuple[int, int] = (50, 38)
    laser_size: tuple[int, int] = (8, 24)
    laser_speed: float = 600.0
    enemy_speed_range: tuple[float, float] = (120.0, 260.0)
    spawn_interval: float = 0.9
    shot_cooldown: float = 0.25
