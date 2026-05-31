from __future__ import annotations

import pygame

from mini_galaxy_defender.assets import load_assets
from mini_galaxy_defender.config import GameSettings
from mini_galaxy_defender.logic import GameState


def run() -> None:
    pygame.init()
    settings = GameSettings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Mini Galaxy Defender")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    assets = load_assets(settings)
    state = GameState(settings=settings)

    running = True
    while running:
        dt = clock.tick(settings.fps) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if state.game_over:
                    state.reset()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                state.fire_laser()

        mouse_x, _ = pygame.mouse.get_pos()
        state.move_player_to(mouse_x)
        state.update(dt)

        screen.blit(assets.background, (0, 0))
        screen.blit(assets.player, (state.player.rect.x, state.player.rect.y))

        for enemy in state.enemies:
            screen.blit(assets.enemy, (enemy.rect.x, enemy.rect.y))
        for laser in state.lasers:
            screen.blit(assets.laser, (laser.rect.x, laser.rect.y))

        score_text = font.render(f"Score: {state.score}", True, (240, 240, 240))
        screen.blit(score_text, (16, 12))

        if state.game_over:
            message = font.render(
                "Game Over - Press R to restart", True, (255, 160, 160)
            )
            message_rect = message.get_rect(
                center=(settings.screen_width / 2, settings.screen_height / 2)
            )
            screen.blit(message, message_rect)

        pygame.display.flip()

    pygame.quit()
