import pygame
import math
from settings import WIDTH, HEIGHT, PLAYER_SPEED, SHIELD_DURATION
from core.assets import get_image

INVINCIBILITY_DURATION = 1000  # ms neranjivosti nakon gubitka života


class Player:
    def __init__(self):
        self.speed = PLAYER_SPEED

        self.image = get_image("player")

        self.x = WIDTH // 2 - self.image.get_width() // 2
        self.y = HEIGHT - self.image.get_height() - 5
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.weapon_level = 1

        self.shield_active = False
        self.shield_end_time = 0

        self.invincible_until = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed

        if self.x < 0:
            self.x = 0
        if self.x + self.image.get_width() > WIDTH:
            self.x = WIDTH - self.image.get_width()

        self.rect.topleft = (self.x, self.y)

    def activate_shield(self):
        self.shield_active = True
        self.shield_end_time = pygame.time.get_ticks() + SHIELD_DURATION

    def is_invincible(self):
        return pygame.time.get_ticks() < self.invincible_until

    def take_hit(self):
        self.invincible_until = pygame.time.get_ticks() + INVINCIBILITY_DURATION

    def update(self):
        if self.shield_active and pygame.time.get_ticks() > self.shield_end_time:
            self.shield_active = False

    def draw_shield_glow(self, screen):
        pulse = math.sin(pygame.time.get_ticks() / 180) * 2
        radius = 52 + int(pulse)

        glow = pygame.Surface((radius * 2 + 20, radius * 2 + 20), pygame.SRCALPHA)
        center = (glow.get_width() // 2, glow.get_height() // 2)

        # blagi spoljašnji sjaj
        pygame.draw.circle(glow, (0, 180, 255, 20), center, radius + 6)

        # glavni prsten
        pygame.draw.circle(glow, (80, 230, 255, 170), center, radius, 3)

        # unutrašnji tanji prsten
        pygame.draw.circle(glow, (180, 255, 255, 90), center, radius - 4, 1)

        glow_rect = glow.get_rect(center=self.rect.center)
        screen.blit(glow, glow_rect)

    def draw(self, screen):
        if self.is_invincible() and (pygame.time.get_ticks() // 100) % 2 == 0:
            return

        if self.shield_active:
            self.draw_shield_glow(screen)

        screen.blit(self.image, (self.x, self.y))