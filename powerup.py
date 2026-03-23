import pygame
from settings import POWERUP_FALL_SPEED

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = 28
        self.height = 28
        self.power_type = power_type   # "shield" ili "weapon"
        self.speed = POWERUP_FALL_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        glow = pygame.Surface((44, 44), pygame.SRCALPHA)

        if self.power_type == "shield":
            pygame.draw.circle(glow, (80, 180, 255, 70), (22, 22), 20)
            screen.blit(glow, (self.x - 8, self.y - 8))
            pygame.draw.circle(screen, (120, 220, 255), self.rect.center, 12)
            pygame.draw.circle(screen, (255, 255, 255), self.rect.center, 6)

        elif self.power_type == "weapon":
            pygame.draw.circle(glow, (255, 220, 90, 70), (22, 22), 20)
            screen.blit(glow, (self.x - 8, self.y - 8))
            pygame.draw.rect(screen, (255, 220, 90), self.rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), (self.x + 9, self.y + 5, 10, 18), border_radius=4)

    def is_off_screen(self, height):
        return self.y > height