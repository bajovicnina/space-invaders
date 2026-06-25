import pygame
from settings import WIDTH, HEIGHT

# putanje
_PLAYER_PATH = "assets/images/playerr.png"
_ENEMY_PATH = "assets/images/green_alien.png"
_BG_PATH = "assets/images/bg5.png"
_STRONG_ENEMY_PATH = "assets/images/yellow_alien.png"
_ELITE_ENEMY_PATH = "assets/images/purple_alien.png"

# cache za slike i fontove
_images = {}
_fonts = {}


def get_image(key):
    return _images.get(key)


def get_font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = pygame.font.Font(path, size)
    return _fonts[key]


def load_all():
    """Pozovi jednom na početku igre, nakon pygame.init() i pygame.display.set_mode()"""

    # player
    img = pygame.image.load(_PLAYER_PATH).convert_alpha()
    _images["player"] = pygame.transform.smoothscale(img, (200, 150))

    # enemy — normalna verzija
    base = pygame.image.load(_ENEMY_PATH).convert_alpha()
    base = pygame.transform.smoothscale(base, (125, 90))
    _images["enemy_normal"] = base

    # enemy — strong verzija
    strong = pygame.image.load(_STRONG_ENEMY_PATH).convert_alpha()
    strong = pygame.transform.smoothscale(strong, (125, 90))
    _images["enemy_strong"] = strong

    # enemy — elite verzija
    elite = pygame.image.load(_ELITE_ENEMY_PATH).convert_alpha()
    elite = pygame.transform.smoothscale(elite, (125, 90))
    _images["enemy_elite"] = elite

    # pozadina
    bg = pygame.image.load(_BG_PATH).convert()
    scale_ratio = min(WIDTH / bg.get_width(), HEIGHT / bg.get_height())
    new_w = int(bg.get_width() * scale_ratio)
    new_h = int(bg.get_height() * scale_ratio)
    _images["bg"] = pygame.transform.smoothscale(bg, (new_w, new_h))
    _images["bg_size"] = (new_w, new_h)