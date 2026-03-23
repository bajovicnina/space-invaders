from enemies.enemy import Enemy
from levels import LEVELS
from settings import RED, WHITE, YELLOW, BLUE

def create_enemies(level):
    config = LEVELS[level]
    enemies = []

    rows = config["enemy_rows"]
    cols = config["enemy_cols"]
    speed = config["enemy_speed"]
    base_hp = config["enemy_hp"]
    spacing_x = 90
    spacing_y = 85
    start_x = 80
    start_y = 50

    stronger_top_row = config.get("stronger_top_row", False)

    for row in range(rows):
        for col in range(cols):
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y

            hp = base_hp
            if stronger_top_row and row == 0:
                hp = base_hp + 1

            enemies.append(
                Enemy(x, y, speed, color=RED, hp=hp, points=10, enemy_type="normal")
            )

    if config.get("weapon_enemy", False):
        enemies.append(
            Enemy(70, 30, speed + 0.35, color=YELLOW, hp=2, points=30, enemy_type="weapon")
        )

    if config.get("shield_enemy", False):
        enemies.append(
            Enemy(620, 30, speed + 0.30, color=BLUE, hp=2, points=20, enemy_type="shield")
        )

    if config.get("bonus_enemy", False):
        enemies.append(
            Enemy(50, 30, speed + 0.4, color=YELLOW, hp=1, points=50, enemy_type="bonus")
        )

    if config.get("forbidden_enemy", False):
        enemies.append(
            Enemy(650, 30, speed + 0.2, color=WHITE, hp=1, points=0, enemy_type="forbidden")
        )

    return enemies