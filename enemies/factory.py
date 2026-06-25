from enemies.enemy import Enemy
from levels import LEVELS
from settings import RED, YELLOW, PURPLE


def create_enemies(level):
    config = LEVELS[level]
    enemies = []

    rows = config["enemy_rows"]
    cols = config["enemy_cols"]
    speed = config["enemy_speed"]
    base_hp = config["enemy_hp"]

    spacing_x = 85
    spacing_y = 65
    start_x = 80
    start_y = 75

    stronger_top_row = config.get("stronger_top_row", False)
    strong_enemy_hp = config.get("strong_enemy_hp", 2)

    for row in range(rows):
        for col in range(cols):
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y

            hp = base_hp
            enemy_type = "normal"
            color = RED
            points = 10

            if level <= 2:
                color = RED
                enemy_type = "normal"
                hp = 1
                points = 10

            elif level in [3, 4]:
                if row == 0:
                    color = YELLOW
                    enemy_type = "yellow"
                    hp = 2
                    points = 20
                else:
                    color = RED
                    enemy_type = "normal"
                    hp = 1
                    points = 10

            elif level in [5, 6]:
                if stronger_top_row and row == 0:
                    color = YELLOW
                    enemy_type = "strong"
                    hp = 2
                    points = 25
                else:
                    color = RED
                    enemy_type = "normal"
                    hp = 1
                    points = 10

            else:
                if row == 0:
                    color = PURPLE
                    enemy_type = "elite"
                    hp = 2
                    points = 30
                elif row == 1:
                    color = YELLOW
                    enemy_type = "yellow"
                    hp = 2
                    points = 20
                else:
                    color = RED
                    enemy_type = "normal"
                    hp = 1
                    points = 10

            enemies.append(
                Enemy(
                    x,
                    y,
                    speed,
                    color=color,
                    hp=hp,
                    points=points,
                    enemy_type=enemy_type
                )
            )

    return enemies