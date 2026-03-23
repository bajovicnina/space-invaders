import pygame
from settings import WIDTH, HEIGHT
from levels import LEVELS

# BOJE
WHITE = (245, 245, 245)
SOFT_BLUE = (140, 200, 255)
GLOW_BLUE = (80, 160, 255)
YELLOW = (255, 220, 120)
GREEN = (120, 255, 170)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)

DARK = (12, 18, 35)
PANEL = (22, 30, 55)
PANEL_HIGHLIGHT = (35, 50, 85)
RED = (255, 110, 110)


def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = current + word + " "
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current.strip())
            current = word + " "

    if current:
        lines.append(current.strip())

    return lines


def get_difficulty(level):
    if level <= 3:
        return "Easy"
    elif level <= 7:
        return "Medium"
    return "Hard"


def get_status(level, unlocked_levels, completed_levels):
    if level in completed_levels:
        return "DONE"
    elif level <= unlocked_levels:
        return "OPEN"
    return "LOCK"


def draw_menu(screen, selected_level, unlocked_levels, completed_levels):
    title_font = pygame.font.SysFont("arial", 54, bold=True)
    subtitle_font = pygame.font.SysFont("arial", 28, bold=True)
    normal_font = pygame.font.SysFont("arial", 24, bold=True)
    small_font = pygame.font.SysFont("arial", 20)
    tiny_font = pygame.font.SysFont("arial", 18, bold=True)

    # title glow
    glow_title = title_font.render("SPACE INVADERS", True, GLOW_BLUE)
    title = title_font.render("SPACE INVADERS", True, WHITE)

    screen.blit(glow_title, (WIDTH // 2 - glow_title.get_width() // 2 + 2, 52))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 48))

    subtitle = subtitle_font.render("Select Level", True, SOFT_BLUE)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 118))

    # dekorativna linija
    pygame.draw.line(screen, SOFT_BLUE, (180, 160), (620, 160), 2)

    # lijevi panel
    list_box = pygame.Rect(60, 190, 250, 320)
    pygame.draw.rect(screen, PANEL, list_box, border_radius=18)
    pygame.draw.rect(screen, SOFT_BLUE, list_box, 2, border_radius=18)

    # desni panel
    info_box = pygame.Rect(340, 190, 400, 320)
    pygame.draw.rect(screen, PANEL, info_box, border_radius=18)
    pygame.draw.rect(screen, SOFT_BLUE, info_box, 2, border_radius=18)

    start_y = 212

    for lvl in LEVELS:
        y = start_y + (lvl - 1) * 28
        is_selected = lvl == selected_level
        is_unlocked = lvl <= unlocked_levels
        is_completed = lvl in completed_levels

        # highlight selected
        if is_selected:
            highlight_rect = pygame.Rect(78, y - 4, 210, 30)
            pygame.draw.rect(screen, PANEL_HIGHLIGHT, highlight_rect, border_radius=10)
            pygame.draw.rect(screen, SOFT_BLUE, highlight_rect, 2, border_radius=10)
            pygame.draw.circle(screen, YELLOW, (92, y + 10), 5)

        # boja level teksta
        if not is_unlocked:
            text_color = GRAY
        elif is_completed:
            text_color = GREEN if not is_selected else YELLOW
        else:
            text_color = YELLOW if is_selected else WHITE

        level_text = normal_font.render(f"Level {lvl}", True, text_color)
        screen.blit(level_text, (105, y))

        # badge
        if is_completed:
            badge = tiny_font.render("DONE", True, GREEN)
            screen.blit(badge, (220, y + 3))
        elif not is_unlocked:
            badge = tiny_font.render("LOCK", True, GRAY)
            screen.blit(badge, (220, y + 3))
        else:
            badge = tiny_font.render("OPEN", True, SOFT_BLUE)
            screen.blit(badge, (220, y + 3))

    # info box content
    level_title = subtitle_font.render(f"Level {selected_level}", True, WHITE)
    screen.blit(level_title, (info_box.x + 20, info_box.y + 18))

    status = get_status(selected_level, unlocked_levels, completed_levels)
    difficulty = get_difficulty(selected_level)
    description = LEVELS[selected_level]["description"]

    status_text = small_font.render(f"Status: {status}", True, LIGHT_GRAY)
    difficulty_text = small_font.render(f"Difficulty: {difficulty}", True, LIGHT_GRAY)

    screen.blit(status_text, (info_box.x + 20, info_box.y + 65))
    screen.blit(difficulty_text, (info_box.x + 20, info_box.y + 95))

    desc_title = normal_font.render("Description", True, SOFT_BLUE)
    screen.blit(desc_title, (info_box.x + 20, info_box.y + 145))

    desc_lines = wrap_text(description, small_font, 350)
    text_y = info_box.y + 185
    for line in desc_lines:
        txt = small_font.render(line, True, WHITE)
        screen.blit(txt, (info_box.x + 20, text_y))
        text_y += 28

    # controls box
    controls_box = pygame.Rect(120, 535, 560, 72)
    pygame.draw.rect(screen, PANEL, controls_box, border_radius=16)
    pygame.draw.rect(screen, SOFT_BLUE, controls_box, 2, border_radius=16)

    controls_font = pygame.font.SysFont("arial", 19, bold=True)
    controls_text = controls_font.render(
        "UP / DOWN - Change level    ENTER - Start    ESC - Exit",
        True,
        WHITE
    )
    screen.blit(
        controls_text,
        (
            WIDTH // 2 - controls_text.get_width() // 2,
            controls_box.y + 24
        )
    )


def draw_level_complete_menu(screen, current_level, unlocked_levels):
    title_font = pygame.font.SysFont("arial", 44, bold=True)
    normal_font = pygame.font.SysFont("arial", 24, bold=True)
    small_font = pygame.font.SysFont("arial", 21)

    box = pygame.Rect(145, 170, 510, 250)
    pygame.draw.rect(screen, PANEL, box, border_radius=18)
    pygame.draw.rect(screen, GREEN, box, 2, border_radius=18)

    glow = title_font.render(f"Level {current_level} Complete!", True, (80, 255, 180))
    title = title_font.render(f"Level {current_level} Complete!", True, WHITE)

    screen.blit(glow, (WIDTH // 2 - glow.get_width() // 2 + 2, 198))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 196))

    info = small_font.render("Choose what you want to do next:", True, LIGHT_GRAY)
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 255))

    options = [
        "N - Next level",
        "R - Restart this level",
        "M - Back to menu"
    ]

    if current_level >= len(LEVELS):
        options[0] = "N - No more levels"

    y = 305
    for option in options:
        txt = normal_font.render(option, True, WHITE)
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y))
        y += 40


def draw_game_over_menu(screen, current_level):
    title_font = pygame.font.SysFont("arial", 44, bold=True)
    normal_font = pygame.font.SysFont("arial", 24, bold=True)
    small_font = pygame.font.SysFont("arial", 21)

    box = pygame.Rect(145, 180, 510, 220)
    pygame.draw.rect(screen, PANEL, box, border_radius=18)
    pygame.draw.rect(screen, RED, box, 2, border_radius=18)

    glow = title_font.render("Game Over", True, (255, 120, 120))
    title = title_font.render("Game Over", True, WHITE)

    screen.blit(glow, (WIDTH // 2 - glow.get_width() // 2 + 2, 205))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 203))

    info = small_font.render(f"You lost on Level {current_level}", True, LIGHT_GRAY)
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 260))

    options = [
        "R - Restart this level",
        "M - Back to menu"
    ]

    y = 310
    for option in options:
        txt = normal_font.render(option, True, WHITE)
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y))
        y += 40