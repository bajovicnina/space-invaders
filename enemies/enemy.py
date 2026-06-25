import pygame
from settings import RED
from core.assets import get_image


class Enemy:
    def __init__(self, x, y, speed, color=RED, hp=1, points=10, enemy_type="normal"):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.hp = hp
        self.max_hp = hp
        self.points = points
        self.enemy_type = enemy_type

        if self.enemy_type == "elite":
            self.image = get_image("enemy_elite")

        elif self.enemy_type == "strong":
            self.image = get_image("enemy_strong")

        elif self.enemy_type == "yellow":
            self.image = get_image("enemy_strong")

        else:
            self.image = get_image("enemy_normal")

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = pygame.Rect(
            self.x + 6,
            self.y + 6,
            self.width - 12,
            self.height - 12
        )

    def move(self, direction):
        self.x += self.speed * direction
        self.rect.topleft = (self.x + 6, self.y + 6)

    def step_down(self, amount):
        self.y += amount
        self.rect.topleft = (self.x + 6, self.y + 6)

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        # Health bar za enemy koji ima više od 1 HP
        if self.max_hp > 1:
            bar_width = 24
            bar_height = 3
            bar_x = self.x + (self.width - bar_width) // 2
            bar_y = self.y + 6

            # pozadina
            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (bar_x, bar_y, bar_width, bar_height),
                border_radius=2
            )

            # boja zavisi od enemy-ja
            if self.enemy_type in ("strong", "yellow"):
                color = (255, 220, 0)      # žuta
            else:
                color = (180, 80, 255)     # ljubičasta

            current_width = int(bar_width * (self.hp / self.max_hp))

            pygame.draw.rect(
                screen,
                color,
                (bar_x, bar_y, current_width, bar_height),
                border_radius=2
            )