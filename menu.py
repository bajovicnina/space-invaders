import pygame
from settings import WIDTH, HEIGHT
from levels import LEVELS

# BOJE
WHITE = (245, 248, 255)
SOFT_BLUE = (150, 210, 255)
GLOW_BLUE = (70, 160, 255)
YELLOW = (255, 220, 120)
GREEN = (120, 255, 170)
GRAY = (140, 150, 170)
LIGHT_GRAY = (205, 215, 235)
RED = (255, 110, 110)

DARK = (7, 12, 28)
PANEL = (18, 28, 58)
PANEL_2 = (24, 36, 72)
PANEL_HIGHLIGHT = (40, 60, 105)
LINE_DARK = (30, 60, 120)


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


def draw_glow_text(screen, text, font, color, x, y, center=False, glow_color=None):
    if glow_color is None:
        glow_color = color

    base = font.render(text, True, color)
    glow = font.render(text, True, glow_color)

    if center:
        x = x - base.get_width() // 2
        y = y - base.get_height() // 2

    # manji, uredniji glow
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        screen.blit(glow, (x + dx, y + dy))

    screen.blit(base, (x, y))


def draw_panel(screen, rect, border_color, fill_color=PANEL, radius=22):
    glow_surface = pygame.Surface((rect.width + 24, rect.height + 24), pygame.SRCALPHA)

    for i, alpha in [(12, 18), (8, 28), (4, 40)]:
        pygame.draw.rect(
            glow_surface,
            (*border_color, alpha),
            (12 - i // 2, 12 - i // 2, rect.width + i, rect.height + i),
            border_radius=radius + 6
        )

    screen.blit(glow_surface, (rect.x - 12, rect.y - 12))

    pygame.draw.rect(screen, fill_color, rect, border_radius=radius)
    inner = rect.inflate(-8, -8)
    pygame.draw.rect(screen, PANEL_2, inner, border_radius=max(10, radius - 6))
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=radius)


def draw_badge(screen, text, color, x, y, font):
    badge_rect = pygame.Rect(x, y, 92, 30)
    pygame.draw.rect(screen, color, badge_rect, border_radius=11)
    inner = badge_rect.inflate(-4, -4)
    pygame.draw.rect(screen, PANEL, inner, border_radius=9)
    pygame.draw.rect(screen, color, badge_rect, 2, border_radius=11)

    txt = font.render(text, True, color)
    screen.blit(
        txt,
        (
            badge_rect.centerx - txt.get_width() // 2,
            badge_rect.centery - txt.get_height() // 2
        )
    )


def draw_stars(screen):
    stars = [
        (55, 65, 2), (120, 115, 1), (210, 70, 2), (305, 105, 1), (415, 82, 2),
        (520, 128, 1), (645, 92, 2), (742, 70, 1), (80, 225, 1), (165, 265, 2),
        (245, 210, 1), (330, 245, 1), (460, 215, 2), (565, 258, 1), (700, 235, 2),
        (95, 395, 2), (190, 350, 1), (290, 410, 2), (395, 365, 1), (525, 398, 1),
        (640, 370, 2), (730, 425, 1), (68, 520, 1), (155, 560, 2), (265, 505, 1),
        (360, 555, 1), (490, 520, 2), (610, 548, 1), (708, 500, 2)
    ]

    for x, y, r in stars:
        pygame.draw.circle(screen, (220, 235, 255), (x, y), r)

    nebula = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(nebula, (60, 120, 255, 28), (130, 500), 120)
    pygame.draw.circle(nebula, (90, 40, 180, 22), (660, 130), 90)
    pygame.draw.circle(nebula, (80, 160, 255, 18), (580, 500), 110)
    screen.blit(nebula, (0, 0))


def draw_background(screen):
    screen.fill(DARK)

    gradient = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for y in range(HEIGHT):
        alpha = int(70 * (y / HEIGHT))
        pygame.draw.line(gradient, (0, 40, 120, alpha), (0, y), (WIDTH, y))
    screen.blit(gradient, (0, 0))

    draw_stars(screen)


def draw_menu(screen, selected_level, unlocked_levels, completed_levels):
    draw_background(screen)

    # FONTOVI - samo 3 varijante
    TITLE_FONT = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 62)
    FONT = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 24)
    SMALL_FONT = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 18)

    # naslov
    draw_glow_text(
        screen,
        "SPACE INVADERS",
        TITLE_FONT,
        WHITE,
        WIDTH // 2,
        76,
        center=True,
        glow_color=GLOW_BLUE
    )

    subtitle = FONT.render("Select Level", True, SOFT_BLUE)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 138))

    pygame.draw.line(screen, SOFT_BLUE, (180, 184), (620, 184), 2)
    pygame.draw.line(screen, LINE_DARK, (180, 188), (620, 188), 1)

    # paneli
    list_box = pygame.Rect(58, 212, 255, 330)
    info_box = pygame.Rect(340, 212, 402, 330)
    controls_box = pygame.Rect(118, 558, 564, 58)

    draw_panel(screen, list_box, SOFT_BLUE)
    draw_panel(screen, info_box, SOFT_BLUE)
    draw_panel(screen, controls_box, SOFT_BLUE, fill_color=(20, 30, 62), radius=18)

    # lijeva lista nivoa
    start_y = 234

    for lvl in LEVELS:
        y = start_y + (lvl - 1) * 29
        is_selected = lvl == selected_level
        is_unlocked = lvl <= unlocked_levels
        is_completed = lvl in completed_levels

        if is_selected:
            highlight_rect = pygame.Rect(list_box.x + 18, y - 4, list_box.width - 36, 30)

            glow_surface = pygame.Surface((highlight_rect.width + 18, highlight_rect.height + 18), pygame.SRCALPHA)
            pygame.draw.rect(
                glow_surface,
                (*SOFT_BLUE, 40),
                (9, 9, highlight_rect.width, highlight_rect.height),
                border_radius=12
            )
            screen.blit(glow_surface, (highlight_rect.x - 9, highlight_rect.y - 9))

            pygame.draw.rect(screen, PANEL_HIGHLIGHT, highlight_rect, border_radius=12)
            pygame.draw.rect(screen, SOFT_BLUE, highlight_rect, 2, border_radius=12)
            pygame.draw.circle(screen, YELLOW, (highlight_rect.x + 16, highlight_rect.centery), 5)

        if not is_unlocked:
            text_color = GRAY
            badge_text = "LOCK"
            badge_color = GRAY
        elif is_completed:
            text_color = YELLOW if is_selected else GREEN
            badge_text = "DONE"
            badge_color = GREEN
        else:
            text_color = YELLOW if is_selected else WHITE
            badge_text = "OPEN"
            badge_color = SOFT_BLUE

        level_text = FONT.render(f"Level {lvl}", True, text_color)
        screen.blit(level_text, (list_box.x + 52, y - 1))

        draw_badge(screen, badge_text, badge_color, list_box.x + 160, y - 2, SMALL_FONT)

    # desni info panel
    level_title = FONT.render(f"Level {selected_level}", True, WHITE)
    screen.blit(level_title, (info_box.x + 24, info_box.y + 18))

    status = get_status(selected_level, unlocked_levels, completed_levels)
    difficulty = get_difficulty(selected_level)
    description = LEVELS[selected_level]["description"]

    if status == "DONE":
        status_color = GREEN
    elif status == "OPEN":
        status_color = SOFT_BLUE
    else:
        status_color = RED

    if difficulty == "Easy":
        diff_color = GREEN
    elif difficulty == "Medium":
        diff_color = YELLOW
    else:
        diff_color = RED

    status_label = SMALL_FONT.render("Status:", True, LIGHT_GRAY)
    diff_label = SMALL_FONT.render("Difficulty:", True, LIGHT_GRAY)

    screen.blit(status_label, (info_box.x + 24, info_box.y + 78))
    screen.blit(diff_label, (info_box.x + 24, info_box.y + 118))

    status_value = SMALL_FONT.render(status, True, status_color)
    diff_value = SMALL_FONT.render(difficulty, True, diff_color)

    screen.blit(status_value, (info_box.x + 120, info_box.y + 78))
    screen.blit(diff_value, (info_box.x + 155, info_box.y + 118))

    pygame.draw.line(
        screen,
        LINE_DARK,
        (info_box.x + 24, info_box.y + 160),
        (info_box.x + info_box.width - 24, info_box.y + 160),
        1
    )

    desc_title = FONT.render("Description", True, SOFT_BLUE)
    screen.blit(desc_title, (info_box.x + 24, info_box.y + 180))

    desc_lines = wrap_text(description, SMALL_FONT, 340)
    text_y = info_box.y + 236
    for line in desc_lines:
        txt = SMALL_FONT.render(line, True, WHITE)
        screen.blit(txt, (info_box.x + 24, text_y))
        text_y += 28

    # controls
    controls_text = SMALL_FONT.render(
        "UP / DOWN - Change level    ENTER - Start    ESC - Exit",
        True,
        WHITE
    )
    screen.blit(
        controls_text,
        (
            WIDTH // 2 - controls_text.get_width() // 2,
            controls_box.y + controls_box.height // 2 - controls_text.get_height() // 2
        )
    )


def draw_level_complete_menu(screen, current_level, unlocked_levels):
    draw_background(screen)

    TITLE_FONT = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 42)
    FONT = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 24)
    SMALL_FONT = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 18)

    box = pygame.Rect(145, 170, 510, 250)
    draw_panel(screen, box, GREEN, fill_color=PANEL, radius=20)

    draw_glow_text(
        screen,
        f"Level {current_level} Complete!",
        TITLE_FONT,
        WHITE,
        WIDTH // 2,
        210,
        center=True,
        glow_color=GREEN
    )

    info = SMALL_FONT.render("Choose what you want to do next:", True, LIGHT_GRAY)
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 258))

    options = [
        "N - Next level",
        "R - Restart this level",
        "M - Back to menu"
    ]

    if current_level >= len(LEVELS):
        options[0] = "N - No more levels"

    y = 305
    for option in options:
        txt = FONT.render(option, True, WHITE)
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y))
        y += 40


def draw_game_over_menu(screen, current_level):
    draw_background(screen)

    TITLE_FONT = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 42)
    FONT = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 24)
    SMALL_FONT = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 18)

    box = pygame.Rect(145, 180, 510, 220)
    draw_panel(screen, box, RED, fill_color=PANEL, radius=20)

    draw_glow_text(
        screen,
        "Game Over",
        TITLE_FONT,
        WHITE,
        WIDTH // 2,
        218,
        center=True,
        glow_color=RED
    )

    info = SMALL_FONT.render(f"You lost on Level {current_level}", True, LIGHT_GRAY)
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 268))

    options = [
        "R - Restart this level",
        "M - Back to menu"
    ]

    y = 315
    for option in options:
        txt = FONT.render(option, True, WHITE)
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y))
        y += 40