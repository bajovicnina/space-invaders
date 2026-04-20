import pygame
from settings import WIDTH, HEIGHT, WHITE

TITLE_FONT_PATH = "assets/fonts/Orbitron-Bold.ttf"
FONT_PATH = "assets/fonts/Orbitron-Regular.ttf"


def draw_text_center(screen, text, size, y):
    font = pygame.font.Font(TITLE_FONT_PATH, 24)
    rendered = font.render(text, True, WHITE)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    screen.blit(rendered, rect)


def draw_hud(screen, score, level, lives, shield_active, weapon_level):
    font = pygame.font.Font(FONT_PATH, 24)

    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    weapon_text = font.render(f"Weapon: {weapon_level}", True, WHITE)
    shield_text = font.render(f"Shield: {'ON' if shield_active else 'OFF'}", True, WHITE)

    screen.blit(score_text, (20, 15))
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 15))
    screen.blit(lives_text, (WIDTH - lives_text.get_width() - 20, 15))
    screen.blit(shield_text, (20, 50))
    screen.blit(weapon_text, (20, 85))


def draw_game_over(screen):
    draw_text_center(screen, "GAME OVER", 54, HEIGHT // 2 - 20)
    draw_text_center(screen, "Press R to restart", 28, HEIGHT // 2 + 30)


def draw_level_complete(screen, level):
    draw_text_center(screen, f"Level {level} complete!", 46, HEIGHT // 2 - 20)
    draw_text_center(screen, "Press N for next level", 28, HEIGHT // 2 + 30)