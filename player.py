import pygame
from settings import WIDTH, HEIGHT, PLAYER_SPEED, SHIELD_DURATION

class Player:
    def __init__(self):
        self.speed = PLAYER_SPEED

        self.image = pygame.image.load("assets/images/playerr.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (200, 150))

        self.x = WIDTH // 2 - self.image.get_width() // 2
        self.y = HEIGHT - self.image.get_height() - 20
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.weapon_level = 1

        self.shield_active = False
        self.shield_end_time = 0

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

    def update(self):
        if self.shield_active and pygame.time.get_ticks() > self.shield_end_time:
            self.shield_active = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        if self.shield_active:
            shield_surface = pygame.Surface(
                (self.image.get_width() + 30, self.image.get_height() + 30),
                pygame.SRCALPHA
            )
            pygame.draw.ellipse(
                shield_surface,
                (100, 200, 255, 70),
                shield_surface.get_rect(),
                width=6
            )
            screen.blit(shield_surface, (self.x - 15, self.y - 15))