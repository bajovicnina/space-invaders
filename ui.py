import pygame
from settings import WIDTH, HEIGHT, WHITE

TITLE_FONT_PATH = "assets/fonts/Orbitron-Bold.ttf"
FONT_PATH = "assets/fonts/Orbitron-Regular.ttf"

_fonts = {}

score_icon = pygame.image.load("assets/images/star.png")
heart_icon = pygame.image.load("assets/images/heart.png")
shield_icon = pygame.image.load("assets/images/shield.png")
weapon_icon = pygame.image.load("assets/images/weapon.png")

score_icon = pygame.transform.smoothscale(score_icon, (30, 30))
heart_icon = pygame.transform.smoothscale(heart_icon, (20, 20))
shield_icon = pygame.transform.smoothscale(shield_icon, (30, 30))
weapon_icon = pygame.transform.smoothscale(weapon_icon, (30, 30))


def get_font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = pygame.font.Font(path, size)
    return _fonts[key]


def draw_text_center(screen, text, size, y):
    font = get_font(TITLE_FONT_PATH, size)
    rendered = font.render(text, True, WHITE)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    screen.blit(rendered, rect)


def draw_hud(screen, score, level, lives, shield_active, weapon_level):
    font = get_font(FONT_PATH, 22)

    hud_bg = pygame.Surface((WIDTH, 90), pygame.SRCALPHA)
    hud_bg.fill((0, 0, 0, 95))
    screen.blit(hud_bg, (0, 0))

    margin = max(int(WIDTH * 0.025), 15)

    # SCORE
    score_x = margin
    screen.blit(score_icon, (score_x, 25))
    score_text = font.render(str(score), True, (255, 220, 80))
    screen.blit(score_text, (score_x + 36, 30))

    # SHIELD
    shield_x = score_x + score_icon.get_width() + 36 + score_text.get_width() + 30
    screen.blit(shield_icon, (shield_x, 25))
    shield_color = (80, 255, 180) if shield_active else (150, 150, 150)
    shield_text = font.render("ON" if shield_active else "OFF", True, shield_color)
    screen.blit(shield_text, (shield_x + 36, 30))

    # LEVEL — centered
    level_text = font.render(f"LEVEL {level}", True, (100, 200, 255))
    level_x = WIDTH // 2 - level_text.get_width() // 2
    screen.blit(level_text, (level_x, 30))

    # HEARTS — right aligned
    heart_spacing = 25
    heart_start_x = WIDTH - margin - (lives * heart_spacing)

    # WEAPON — left of hearts
    weapon_text = font.render(str(weapon_level), True, (220, 120, 255))
    weapon_width = weapon_icon.get_width() + 36 + weapon_text.get_width()

    weapon_x = heart_start_x - weapon_width - 45

    screen.blit(weapon_icon, (weapon_x, 25))
    screen.blit(weapon_text, (weapon_x + 36, 30))

    # HEARTS
    for i in range(lives):
        screen.blit(heart_icon, (heart_start_x + i * heart_spacing, 35))