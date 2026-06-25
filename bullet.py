import pygame
from settings import BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED


class Bullet:
    def __init__(self, x, y, dx=0):
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT

        self.x = x
        self.y = y

        self.dx = dx          # horizontalno kretanje
        self.speed = BULLET_SPEED

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x += self.dx
        self.y -= self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        glow_surface = pygame.Surface(
            (self.width + 12, self.height + 12),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            glow_surface,
            (255, 0, 0, 60),
            (0, 0, self.width + 12, self.height + 12),
            border_radius=6
        )

        pygame.draw.rect(
            glow_surface,
            (255, 80, 80, 120),
            (3, 3, self.width + 6, self.height + 6),
            border_radius=4
        )

        pygame.draw.rect(
            glow_surface,
            (255, 255, 255),
            (6, 6, self.width, self.height),
            border_radius=3
        )

        screen.blit(glow_surface, (self.x - 6, self.y - 6))

    def is_off_screen(self):
        return self.y < 0 or self.x < -20 or self.x > 820