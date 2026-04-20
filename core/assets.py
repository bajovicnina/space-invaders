import pygame
from settings import WIDTH, HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT


BACKGROUND_PATH = 'assets/images/background3.jpg'
PLAYER_PATH = 'assets/images/player1.png'
ENEMY_PATH = 'assets/images/alien4.png'


def load_scaled_image(path: str, size: tuple[int, int], alpha: bool = True) -> pygame.Surface:
    image = pygame.image.load(path)
    image = image.convert_alpha() if alpha else image.convert()
    return pygame.transform.scale(image, size)


def tint_image(image: pygame.Surface, color: tuple[int, int, int], alpha: int = 80) -> pygame.Surface:
    tinted = image.copy()
    overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    overlay.fill((color[0], color[1], color[2], alpha))
    tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return tinted


def load_background() -> pygame.Surface:
    return load_scaled_image(BACKGROUND_PATH, (WIDTH, HEIGHT), alpha=False)


def load_player_image() -> pygame.Surface:
    return load_scaled_image(PLAYER_PATH, (PLAYER_WIDTH, PLAYER_HEIGHT))


def load_enemy_images() -> dict[str, pygame.Surface]:
    basic = load_scaled_image(ENEMY_PATH, (ENEMY_WIDTH, ENEMY_HEIGHT))
    medium = tint_image(basic, (80, 120, 255), 70)
    strong = tint_image(basic, (180, 80, 255), 90)

    return {
        'basic': basic,
        'medium': medium,
        'strong': strong,
    }
