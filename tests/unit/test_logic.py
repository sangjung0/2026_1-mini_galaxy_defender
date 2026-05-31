import random

from mini_galaxy_defender.config import GameSettings
from mini_galaxy_defender.logic import Enemy, GameState, Laser, Rect


def make_settings() -> GameSettings:
    return GameSettings(spawn_interval=999.0)


def test_player_move_clamps_to_bounds() -> None:
    state = GameState(settings=make_settings())
    state.move_player_to(-100)
    assert state.player.rect.x == 0

    state.move_player_to(state.settings.screen_width + 200)
    expected = state.settings.screen_width - state.player.rect.width
    assert state.player.rect.x == expected


def test_fire_laser_respects_cooldown() -> None:
    state = GameState(settings=make_settings())
    assert state.fire_laser() is True
    assert state.fire_laser() is False

    state.update(state.settings.shot_cooldown)
    assert state.fire_laser() is True


def test_spawn_enemy_within_bounds() -> None:
    rng = random.Random(7)
    state = GameState(settings=make_settings(), rng=rng)
    enemy = state.spawn_enemy()

    assert enemy.rect.x >= 0
    assert enemy.rect.x <= state.settings.screen_width - enemy.rect.width
    assert enemy.rect.y == -enemy.rect.height


def test_collision_removes_enemy_and_laser() -> None:
    state = GameState(settings=make_settings())
    enemy_rect = Rect(100, 100, 40, 40)
    laser_rect = Rect(110, 110, 8, 24)

    state.enemies.append(Enemy(rect=enemy_rect, speed=0))
    state.lasers.append(Laser(rect=laser_rect, speed=0))
    state.update(0)

    assert state.score == 100
    assert state.enemies == []
    assert state.lasers == []


def test_game_over_when_enemy_leaves_screen() -> None:
    state = GameState(settings=make_settings())
    enemy_rect = Rect(50, state.settings.screen_height + 10, 40, 40)
    state.enemies.append(Enemy(rect=enemy_rect, speed=0))
    state.update(0)

    assert state.game_over is True
