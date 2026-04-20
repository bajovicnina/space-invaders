import pygame
from settings import RED

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

        # bira sliku po tipu enemyja
        if self.enemy_type == "strong":
            self.image = pygame.image.load("assets/images/enemy2.png").convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (110, 80))
        else:
            self.image = pygame.image.load("assets/images/green_alien.png").convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (110, 80))

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # manji hitbox da bolje odgovara alienu
        self.rect = pygame.Rect(self.x + 12, self.y + 10, self.width - 24, self.height - 20)

    def move(self):
        self.y += self.speed
        self.rect.topleft = (self.x + 12, self.y + 10)

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        # HP bar za enemyje koji se gadjaju vise puta
        if self.max_hp > 1:
            bar_width = self.width
            bar_height = 8
            fill_width = int((self.hp / self.max_hp) * bar_width)

            pygame.draw.rect(screen, (60, 60, 60), (self.x, self.y - 12, bar_width, bar_height))
            pygame.draw.rect(screen, (180, 80, 255), (self.x, self.y - 12, fill_width, bar_height))

        # highlight za specijalne enemyje
        if self.enemy_type == "weapon":
            pygame.draw.rect(screen, (255, 220, 80), (self.x, self.y, self.width, self.height), 3)

        elif self.enemy_type == "shield":
            pygame.draw.rect(screen, (80, 200, 255), (self.x, self.y, self.width, self.height), 3)

        elif self.enemy_type == "bonus":
            pygame.draw.rect(screen, (255, 150, 255), (self.x, self.y, self.width, self.height), 3)

        elif self.enemy_type == "forbidden":
            pygame.draw.rect(screen, (255, 80, 80), (self.x, self.y, self.width, self.height), 3)

        elif self.enemy_type == "strong":
            pygame.draw.rect(screen, (170, 100, 255), (self.x, self.y, self.width, self.height), 3)