from __future__ import annotations

import random

from dataclasses import dataclass, field

from mini_galaxy_defender.config import GameSettings


@dataclass
class Rect:
    x: float
    y: float
    width: float
    height: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    def intersects(self, other: Rect) -> bool:
        return not (
            self.right <= other.left
            or self.left >= other.right
            or self.bottom <= other.top
            or self.top >= other.bottom
        )


@dataclass
class Laser:
    rect: Rect
    speed: float

    def update(self, dt: float) -> None:
        self.rect.y -= self.speed * dt


@dataclass
class Enemy:
    rect: Rect
    speed: float

    def update(self, dt: float) -> None:
        self.rect.y += self.speed * dt


@dataclass
class Player:
    rect: Rect


@dataclass
class GameState:
    settings: GameSettings = field(default_factory=GameSettings)
    rng: random.Random = field(default_factory=random.Random)
    score: int = 0
    game_over: bool = False
    enemies: list[Enemy] = field(default_factory=list)
    lasers: list[Laser] = field(default_factory=list)
    spawn_timer: float = 0.0
    shot_timer: float = 0.0
    player: Player = field(init=False)

    def __post_init__(self) -> None:
        self.player = self._create_player()
        self.shot_timer = self.settings.shot_cooldown

    def _create_player(self) -> Player:
        width, height = self.settings.player_size
        x = (self.settings.screen_width - width) / 2
        y = self.settings.screen_height - height - 20
        return Player(rect=Rect(x=x, y=y, width=width, height=height))

    def reset(self) -> None:
        self.score = 0
        self.game_over = False
        self.enemies.clear()
        self.lasers.clear()
        self.spawn_timer = 0.0
        self.shot_timer = self.settings.shot_cooldown
        self.player = self._create_player()

    def move_player_to(self, x: float) -> None:
        width = self.player.rect.width
        min_x = 0.0
        max_x = self.settings.screen_width - width
        clamped = max(min_x, min(max_x, x - width / 2))
        self.player.rect.x = clamped

    def can_fire(self) -> bool:
        return (not self.game_over) and self.shot_timer >= self.settings.shot_cooldown

    def fire_laser(self) -> bool:
        if not self.can_fire():
            return False
        laser_width, laser_height = self.settings.laser_size
        laser_x = self.player.rect.center_x - laser_width / 2
        laser_y = self.player.rect.y - laser_height + 8
        self.lasers.append(
            Laser(
                rect=Rect(
                    x=laser_x,
                    y=laser_y,
                    width=laser_width,
                    height=laser_height,
                ),
                speed=self.settings.laser_speed,
            )
        )
        self.shot_timer = 0.0
        return True

    def spawn_enemy(self) -> Enemy:
        enemy_width, enemy_height = self.settings.enemy_size
        max_x = self.settings.screen_width - enemy_width
        x = self.rng.uniform(0, max_x)
        y = -enemy_height
        min_speed, max_speed = self.settings.enemy_speed_range
        speed = self.rng.uniform(min_speed, max_speed)
        enemy = Enemy(
            rect=Rect(x=x, y=y, width=enemy_width, height=enemy_height), speed=speed
        )
        self.enemies.append(enemy)
        return enemy

    def update(self, dt: float) -> None:
        if self.game_over:
            return

        self.spawn_timer += dt
        self.shot_timer += dt

        while self.spawn_timer >= self.settings.spawn_interval:
            self.spawn_timer -= self.settings.spawn_interval
            self.spawn_enemy()

        for laser in self.lasers:
            laser.update(dt)
        for enemy in self.enemies:
            enemy.update(dt)

        self.lasers = [laser for laser in self.lasers if laser.rect.bottom >= 0]

        remaining_enemies: list[Enemy] = []
        remaining_lasers: list[Laser] = []
        consumed_lasers: set[int] = set()

        for enemy in self.enemies:
            if enemy.rect.top > self.settings.screen_height:
                self.game_over = True
                continue

            hit = False
            for index, laser in enumerate(self.lasers):
                if index in consumed_lasers:
                    continue
                if laser.rect.intersects(enemy.rect):
                    consumed_lasers.add(index)
                    hit = True
                    self.score += 100
                    break
            if not hit:
                remaining_enemies.append(enemy)

        for index, laser in enumerate(self.lasers):
            if index not in consumed_lasers:
                remaining_lasers.append(laser)

        self.enemies = remaining_enemies
        self.lasers = remaining_lasers
