import pygame
from settings import WIDTH, HEIGHT
from levels import LEVELS
from ui import get_font
from core.assets import get_image

logo_enemy = None


WHITE = (245, 248, 255)
SOFT_BLUE = (150, 210, 255)
CYAN = (0, 190, 255)
YELLOW = (255, 220, 120)
GREEN = (120, 255, 170)
GRAY = (140, 150, 170)
LIGHT_GRAY = (205, 215, 235)
RED = (255, 110, 110)

DARK = (7, 12, 28)
PANEL = (10, 18, 38)
PANEL_HIGHLIGHT = (18, 55, 105)
LINE_DARK = (25, 55, 105)


def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = current + word + " "
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
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
        x -= base.get_width() // 2
        y -= base.get_height() // 2

    for offset in [2]:
        alpha_glow = glow.copy()
        alpha_glow.set_alpha(35)

        for dx, dy in [
            (-offset, 0), (offset, 0),
            (0, -offset), (0, offset),
            (-offset, -offset), (offset, offset),
            (-offset, offset), (offset, -offset)
        ]:
            screen.blit(alpha_glow, (x + dx, y + dy))

    mid = glow.copy()
    mid.set_alpha(90)

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        screen.blit(mid, (x + dx, y + dy))

    screen.blit(base, (x, y))


def draw_panel(screen, rect, border_color, fill_color=PANEL, radius=24):
    glow_surface = pygame.Surface((rect.width + 28, rect.height + 28), pygame.SRCALPHA)

    for i, alpha in [(14, 16), (9, 26), (5, 38)]:
        pygame.draw.rect(
            glow_surface,
            (*border_color, alpha),
            (14 - i // 2, 14 - i // 2, rect.width + i, rect.height + i),
            border_radius=radius + 8
        )

    screen.blit(glow_surface, (rect.x - 14, rect.y - 14))
    pygame.draw.rect(screen, (*fill_color, 205), rect, border_radius=radius)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=radius)

    inner = rect.inflate(-10, -10)
    pygame.draw.rect(screen, (20, 38, 80, 80), inner, width=1, border_radius=max(10, radius - 8))


def draw_button(screen, rect, text, font, is_selected=False, color=CYAN):
    if is_selected:
        glow = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*color, 42), (10, 10, rect.width, rect.height), border_radius=16)
        screen.blit(glow, (rect.x - 10, rect.y - 10))
        pygame.draw.rect(screen, PANEL_HIGHLIGHT, rect, border_radius=14)
        pygame.draw.rect(screen, color, rect, 2, border_radius=14)

        pygame.draw.polygon(
            screen,
            GREEN,
            [
                (rect.x + 20, rect.centery - 9),
                (rect.x + 20, rect.centery + 9),
                (rect.x + 35, rect.centery)
            ]
        )
        txt_color = WHITE
    else:
        pygame.draw.rect(screen, (*PANEL, 190), rect, border_radius=14)
        pygame.draw.rect(screen, (*GRAY, 120), rect, 1, border_radius=14)
        txt_color = GRAY

    label = font.render(text, True, txt_color)
    screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))


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
    screen.blit(get_image("bg"), (0, 0))


def _load_logo_enemies():
    global logo_enemy

    if logo_enemy is None:
        logo_enemy = {
            "green": pygame.transform.smoothscale(
                pygame.image.load("assets/images/green_alien.png").convert_alpha(),
                (165, 125)
            ),
            "yellow": pygame.transform.smoothscale(
                pygame.image.load("assets/images/yellow_alien.png").convert_alpha(),
                (120, 90)
            ),
            "purple": pygame.transform.smoothscale(
                pygame.image.load("assets/images/purple_alien.png").convert_alpha(),
                (120, 90)
            )
        }


def draw_header(screen, subtitle=None):
    _load_logo_enemies()

    title_font = get_font("assets/fonts/Orbitron-Bold.ttf", 54)
    small_font = get_font("assets/fonts/Orbitron-Regular.ttf", 18)
    center_x = WIDTH // 2

    screen.blit(logo_enemy["yellow"], (center_x - 185, 18))
    screen.blit(logo_enemy["green"], (center_x - 82, 0))
    screen.blit(logo_enemy["purple"], (center_x + 70, 18))

    draw_glow_text(
        screen,
        "SPACE INVADERS",
        title_font,
        (220, 245, 255),
        WIDTH // 2,
        150,
        center=True,
        glow_color=(0, 150, 255)
    )

    if subtitle:
        sub = small_font.render(subtitle, True, CYAN)
        sub_x = WIDTH // 2 - sub.get_width() // 2
        screen.blit(sub, (sub_x, 188))
        pygame.draw.line(screen, CYAN, (sub_x - 90, 199), (sub_x - 20, 199), 2)
        pygame.draw.line(screen, CYAN, (sub_x + sub.get_width() + 20, 199), (sub_x + sub.get_width() + 90, 199), 2)


def draw_main_menu(screen, selected_option, unlocked_levels, completed_levels):
    draw_background(screen)
    draw_header(screen)

    font = get_font("assets/fonts/Orbitron-Regular.ttf", 28)
    small_font = get_font("assets/fonts/Orbitron-Regular.ttf", 15)

    next_playable = min(unlocked_levels, len(LEVELS))
    diff = get_difficulty(next_playable)
    desc = LEVELS[next_playable]["description"]
    diff_color = GREEN if diff == "Easy" else YELLOW if diff == "Medium" else RED

    panel = pygame.Rect(220, 220, 360, 340)
    draw_panel(screen, panel, CYAN)

    level_label = small_font.render(f"CURRENT LEVEL: {next_playable}", True, CYAN)
    screen.blit(level_label, (panel.centerx - level_label.get_width() // 2, panel.y + 22))

    diff_label = small_font.render("DIFFICULTY: ", True, GRAY)
    diff_val = small_font.render(diff, True, diff_color)
    diff_x = panel.centerx - (diff_label.get_width() + diff_val.get_width()) // 2
    screen.blit(diff_label, (diff_x, panel.y + 46))
    screen.blit(diff_val, (diff_x + diff_label.get_width(), panel.y + 46))

    pygame.draw.line(screen, LINE_DARK, (panel.x + 24, panel.y + 72), (panel.right - 24, panel.y + 72), 1)

    btn_w = 280
    btn_h = 52
    btn_x = panel.centerx - btn_w // 2
    btn_y_start = panel.y + 90
    labels = ["PLAY", "LEVELS", "EXIT"]
    colors = [GREEN, CYAN, RED]

    mouse_pos = pygame.mouse.get_pos()
    for i, (label, color) in enumerate(zip(labels, colors)):
        btn_rect = pygame.Rect(btn_x, btn_y_start + i * 70, btn_w, btn_h)
        active = selected_option == i or btn_rect.collidepoint(mouse_pos)
        draw_button(screen, btn_rect, label, font, active, color)

    hint_font = get_font("assets/fonts/Orbitron-Regular.ttf", 14)
    hint = hint_font.render("CLICK A BUTTON TO CONTINUE", True, GRAY)
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 595))


def draw_level_select(screen, selected_level, unlocked_levels, completed_levels):
    draw_background(screen)
    draw_header(screen, "S E L E C T   L E V E L")

    font = get_font("assets/fonts/Orbitron-Regular.ttf", 22)
    small_font = get_font("assets/fonts/Orbitron-Regular.ttf", 16)
    big_font = get_font("assets/fonts/Orbitron-Bold.ttf", 30)
    badge_font = get_font("assets/fonts/Orbitron-Regular.ttf", 13)
    button_font = get_font("assets/fonts/Orbitron-Regular.ttf", 18)

    list_box = pygame.Rect(55, 218, 310, 315)
    info_box = pygame.Rect(390, 218, 355, 315)

    draw_panel(screen, list_box, CYAN)
    draw_panel(screen, info_box, CYAN)

    row_x = list_box.x + 18
    row_y = list_box.y + 22
    row_w = list_box.width - 36
    row_h = 30
    row_gap = 29
    mouse_pos = pygame.mouse.get_pos()

    for lvl in LEVELS:
        row_rect = pygame.Rect(row_x, row_y + (lvl - 1) * row_gap, row_w, row_h)
        is_selected = lvl == selected_level or row_rect.collidepoint(mouse_pos)
        is_unlocked = lvl <= unlocked_levels
        is_completed = lvl in completed_levels

        if is_selected:
            glow = pygame.Surface((row_rect.width + 14, row_rect.height + 14), pygame.SRCALPHA)
            pygame.draw.rect(glow, (0, 190, 255, 45), (7, 7, row_rect.width, row_rect.height), border_radius=10)
            screen.blit(glow, (row_rect.x - 7, row_rect.y - 7))
            pygame.draw.rect(screen, PANEL_HIGHLIGHT, row_rect, border_radius=10)
            pygame.draw.rect(screen, CYAN, row_rect, 2, border_radius=10)
            pygame.draw.polygon(screen, GREEN, [
                (row_rect.x + 14, row_rect.centery - 8),
                (row_rect.x + 14, row_rect.centery + 8),
                (row_rect.x + 28, row_rect.centery)
            ])
        else:
            pygame.draw.line(screen, LINE_DARK, (row_rect.x + 8, row_rect.bottom), (row_rect.right - 8, row_rect.bottom), 1)

        if not is_unlocked:
            text_color = GRAY
            badge_text = "LOCK"
            badge_color = (100, 115, 140)
        elif is_completed:
            text_color = WHITE
            badge_text = "DONE"
            badge_color = GREEN
        else:
            text_color = WHITE
            badge_text = "OPEN"
            badge_color = CYAN

        level_text = font.render(f"Level {lvl}", True, text_color)
        screen.blit(level_text, (row_rect.x + 38, row_rect.y + 4))

        badge_rect = pygame.Rect(row_rect.right - 68, row_rect.y + 4, 62, 22)
        pygame.draw.rect(screen, PANEL, badge_rect, border_radius=6)
        pygame.draw.rect(screen, badge_color, badge_rect, 1, border_radius=6)
        btxt = badge_font.render(badge_text, True, badge_color)
        screen.blit(btxt, (badge_rect.centerx - btxt.get_width() // 2, badge_rect.centery - btxt.get_height() // 2))

    difficulty = get_difficulty(selected_level)
    status = get_status(selected_level, unlocked_levels, completed_levels)
    description = LEVELS[selected_level]["description"]

    level_title = big_font.render(f"LEVEL {selected_level}", True, WHITE)
    screen.blit(level_title, (info_box.x + 26, info_box.y + 22))

    status_color = GREEN if status == "DONE" else CYAN if status == "OPEN" else RED
    diff_color = GREEN if difficulty == "Easy" else YELLOW if difficulty == "Medium" else RED

    pygame.draw.line(screen, LINE_DARK, (info_box.x + 26, info_box.y + 68), (info_box.right - 26, info_box.y + 68), 1)

    for i, (label, value, val_color) in enumerate([
        ("STATUS", status, status_color),
        ("DIFFICULTY", difficulty, diff_color)
    ]):
        y_offset = info_box.y + 84 + i * 42
        pygame.draw.circle(screen, CYAN, (info_box.x + 22, y_offset + 10), 7, 1)
        l = small_font.render(label + ":", True, CYAN)
        v = small_font.render(value, True, val_color)
        screen.blit(l, (info_box.x + 36, y_offset))
        screen.blit(v, (info_box.x + 180, y_offset))

    pygame.draw.line(screen, LINE_DARK, (info_box.x + 26, info_box.y + 182), (info_box.right - 26, info_box.y + 182), 1)

    desc_title = small_font.render("DESCRIPTION", True, CYAN)
    screen.blit(desc_title, (info_box.x + 26, info_box.y + 196))

    text_y = info_box.y + 224
    for line in wrap_text(description, small_font, info_box.width - 52):
        t = small_font.render(line, True, WHITE)
        screen.blit(t, (info_box.x + 26, text_y))
        text_y += 24

    start_rect = pygame.Rect(150, 548, 220, 42)
    back_rect = pygame.Rect(430, 548, 220, 42)
    can_start = selected_level <= unlocked_levels

    draw_button(screen, start_rect, "PLAY LEVEL", button_font, can_start, GREEN if can_start else GRAY)
    draw_button(screen, back_rect, "BACK", button_font, back_rect.collidepoint(mouse_pos), CYAN)

def draw_level_complete_menu(screen, current_level, unlocked_levels):
    draw_background(screen)

    title_font = get_font("assets/fonts/Orbitron-Bold.ttf", 40)
    font = get_font("assets/fonts/Orbitron-Regular.ttf", 20)
    small_font = get_font("assets/fonts/Orbitron-Regular.ttf", 15)

    has_next = current_level < len(LEVELS)
    main_box = pygame.Rect(80, 145, 640, 430) if has_next else pygame.Rect(145, 170, 510, 280)

    draw_panel(screen, main_box, GREEN, fill_color=PANEL, radius=20)

    draw_glow_text(
        screen,
        f"Level {current_level} Complete!",
        title_font,
        WHITE,
        WIDTH // 2,
        185,
        center=True,
        glow_color=GREEN
    )

    mouse_pos = pygame.mouse.get_pos()

    if has_next:
        action_x = main_box.x + 30
        action_top = 238

        info_lbl = small_font.render("What next?", True, LIGHT_GRAY)
        screen.blit(info_lbl, (action_x, action_top))

        options = [
            ("NEXT LEVEL", GREEN),
            ("RESTART", CYAN),
            ("BACK TO MENU", RED)
        ]

        for i, (label, color) in enumerate(options):
            y = action_top + 36 + i * 65
            btn_rect = pygame.Rect(action_x, y, 250, 40)
            draw_button(screen, btn_rect, label, font, True or btn_rect.collidepoint(mouse_pos), color)

        sep_x = main_box.x + main_box.width // 2 - 10
        pygame.draw.line(screen, LINE_DARK, (sep_x, 230), (sep_x, main_box.bottom - 24), 1)

        next_lvl = current_level + 1
        next_diff = get_difficulty(next_lvl)
        next_desc = LEVELS[next_lvl]["description"]
        next_diff_color = GREEN if next_diff == "Easy" else YELLOW if next_diff == "Medium" else RED

        info_x = sep_x + 24
        big_font = get_font("assets/fonts/Orbitron-Bold.ttf", 26)
        next_title = big_font.render(f"LEVEL {next_lvl}", True, CYAN)
        screen.blit(next_title, (info_x, 255))

        diff_label = small_font.render("DIFFICULTY: ", True, GRAY)
        diff_val = small_font.render(next_diff, True, next_diff_color)
        screen.blit(diff_label, (info_x, 295))
        screen.blit(diff_val, (info_x + diff_label.get_width(), 295))

        pygame.draw.line(screen, LINE_DARK, (info_x, 325), (main_box.right - 26, 325), 1)

        desc_lbl = small_font.render("DESCRIPTION", True, CYAN)
        screen.blit(desc_lbl, (info_x, 337))

        ty = 365
        for line in wrap_text(next_desc, small_font, main_box.right - info_x - 30):
            t = small_font.render(line, True, WHITE)
            screen.blit(t, (info_x, ty))
            ty += 22

    else:
        info = small_font.render("You've completed all levels!", True, LIGHT_GRAY)
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 248))

        options = [("RESTART", CYAN), ("BACK TO MENU", RED)]
        for i, (label, color) in enumerate(options):
            y = 300 + i * 48
            btn_rect = pygame.Rect(WIDTH // 2 - 130, y, 260, 40)
            draw_button(screen, btn_rect, label, font, True or btn_rect.collidepoint(mouse_pos), color)


def draw_game_over_menu(screen, current_level):
    draw_background(screen)

    title_font = get_font("assets/fonts/Orbitron-Bold.ttf", 42)
    font = get_font("assets/fonts/Orbitron-Regular.ttf", 20)
    small_font = get_font("assets/fonts/Orbitron-Regular.ttf", 15)

    box = pygame.Rect(155, 175, 490, 240)
    draw_panel(screen, box, RED, fill_color=PANEL, radius=20)

    draw_glow_text(
        screen,
        "Game Over",
        title_font,
        WHITE,
        WIDTH // 2,
        210,
        center=True,
        glow_color=RED
    )

    info = small_font.render(f"You lost on Level {current_level}", True, LIGHT_GRAY)
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 264))

    mouse_pos = pygame.mouse.get_pos()
    action_x = WIDTH // 2 - 150
    options = [("RESTART", CYAN), ("BACK TO MENU", RED)]

    for i, (label, color) in enumerate(options):
        y = 308 + i * 48
        btn_rect = pygame.Rect(action_x, y, 300, 40)
        draw_button(screen, btn_rect, label, font, True or btn_rect.collidepoint(mouse_pos), color)
