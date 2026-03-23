import pygame
from settings import ENEMY_BULLET_SPEED

class EnemyBullet:
    def __init__(self, x, y):
        self.width = 6
        self.height = 18
        self.x = x
        self.y = y
        self.speed = ENEMY_BULLET_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        glow = pygame.Surface((16, 28), pygame.SRCALPHA)
        pygame.draw.rect(glow, (255, 80, 80, 80), (0, 0, 16, 28), border_radius=6)
        screen.blit(glow, (self.x - 5, self.y - 5))
        pygame.draw.rect(screen, (255, 120, 120), self.rect, border_radius=3)

    def is_off_screen(self, height):
        return self.y > height