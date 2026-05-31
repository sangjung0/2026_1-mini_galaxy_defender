from __future__ import annotations

import pygame

from dataclasses import dataclass
from pathlib import Path

from mini_galaxy_defender.config import GameSettings

ASSET_ROOT = Path("assets/kenney_space-shooter-remastered")


@dataclass(frozen=True)
class GameAssets:
    background: pygame.Surface
    player: pygame.Surface
    enemy: pygame.Surface
    laser: pygame.Surface


def _load_image(path: Path, *, alpha: bool) -> pygame.Surface:
    if alpha:
        return pygame.image.load(str(path)).convert_alpha()
    return pygame.image.load(str(path)).convert()


def load_assets(settings: GameSettings) -> GameAssets:
    background_path = ASSET_ROOT / "Backgrounds" / "darkPurple.png"
    player_path = ASSET_ROOT / "PNG" / "playerShip1_blue.png"
    enemy_path = ASSET_ROOT / "PNG" / "Enemies" / "enemyRed2.png"
    laser_path = ASSET_ROOT / "PNG" / "Lasers" / "laserBlue08.png"

    background = _load_image(background_path, alpha=False)
    background = pygame.transform.scale(
        background, (settings.screen_width, settings.screen_height)
    )
    player = _load_image(player_path, alpha=True)
    player = pygame.transform.scale(player, settings.player_size)
    enemy = _load_image(enemy_path, alpha=True)
    enemy = pygame.transform.scale(enemy, settings.enemy_size)
    laser = _load_image(laser_path, alpha=True)
    laser = pygame.transform.scale(laser, settings.laser_size)

    return GameAssets(
        background=background,
        player=player,
        enemy=enemy,
        laser=laser,
    )
