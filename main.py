import pygame
import random

from settings import WIDTH, HEIGHT, FPS
from player import Player
from bullet import Bullet
from enemy_bullet import EnemyBullet
from powerup import PowerUp
from enemies.factory import create_enemies
from levels import LEVELS
from ui import draw_hud
# IZMJENA: draw_menu ne postoji u menu.py — zamijenjeno sa draw_main_menu i draw_level_select
from menu import draw_main_menu, draw_level_select, draw_level_complete_menu, draw_game_over_menu

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
powerup_sound = pygame.mixer.Sound("assets/sounds/powerup.wav")
explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
explosion_sound.set_volume(0.5)

SHOOT_COOLDOWN = 300
last_shot_time = 0

EDGE_MARGIN = 40
STEP_DOWN_AMOUNT = 3
ENEMY_H_SPEED_MULTIPLIER = 2
MAX_ENEMY_BULLETS = 2

from core.assets import load_all, get_image
load_all()

bg = get_image("bg")
new_w, new_h = get_image("bg_size")
bg_x = (WIDTH - new_w) // 2
bg_y = (HEIGHT - new_h) // 2

overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.set_alpha(25)
overlay.fill((10, 20, 50))


def center_enemies(enemies):
    if not enemies:
        return enemies

    min_x = min(enemy.x for enemy in enemies)
    max_x = max(enemy.x + enemy.width for enemy in enemies)
    group_width = max_x - min_x
    shift_x = (WIDTH - group_width) // 2 - min_x

    for enemy in enemies:
        enemy.x += shift_x
        enemy.rect.x = enemy.x

    return enemies


def start_level(level, lives=6):
    player = Player()
    bullets = []
    enemies = center_enemies(create_enemies(level))
    enemy_bullets = []
    powerups = []
    return player, bullets, enemies, enemy_bullets, powerups, lives


current_level = 1
selected_level = 1
unlocked_levels = 1
completed_levels = set()
enemy_direction = 1

selected_option = 0

player, bullets, enemies, enemy_bullets, powerups, lives = start_level(current_level, 3)
score = 0
score_change = ""
score_change_time = 0
score_change_y = 58

game_state = "main_menu"
running = True



def get_main_menu_buttons():
    btn_w = 280
    btn_h = 52
    btn_x = 220 + 360 // 2 - btn_w // 2
    btn_y_start = 220 + 90
    return [
        pygame.Rect(btn_x, btn_y_start + 0 * 70, btn_w, btn_h),  # PLAY
        pygame.Rect(btn_x, btn_y_start + 1 * 70, btn_w, btn_h),  # LEVELS
        pygame.Rect(btn_x, btn_y_start + 2 * 70, btn_w, btn_h),  # EXIT
    ]


def get_level_rows():
    list_box = pygame.Rect(55, 218, 310, 345)
    row_x = list_box.x + 18
    row_y = list_box.y + 22
    row_w = list_box.width - 36
    row_h = 30
    row_gap = 29
    rows = {}
    for lvl in LEVELS:
        rows[lvl] = pygame.Rect(row_x, row_y + (lvl - 1) * row_gap, row_w, row_h)
    return rows


def get_level_select_buttons():
    return {
        "start": pygame.Rect(150, 548, 220, 42),
        "back": pygame.Rect(430, 548, 220, 42),
    }


def get_level_complete_buttons():
    if current_level < len(LEVELS):
        action_x = 80 + 30
        action_top = 238
        return {
            "next": pygame.Rect(action_x, action_top + 36, 250, 40),
            "restart": pygame.Rect(action_x, action_top + 36 + 48, 250, 40),
            "menu": pygame.Rect(action_x, action_top + 36 + 96, 250, 40),
        }
    else:
        action_x = WIDTH // 2 - 130
        return {
            "restart": pygame.Rect(action_x, 300, 260, 40),
            "menu": pygame.Rect(action_x, 348, 260, 40),
        }


def get_game_over_buttons():
    action_x = WIDTH // 2 - 150
    return {
        "restart": pygame.Rect(action_x, 308, 300, 40),
        "menu": pygame.Rect(action_x, 356, 300, 40),
    }

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # HOVER EFEKAT ZA MIŠ
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos

            if game_state == "main_menu":
                for i, rect in enumerate(get_main_menu_buttons()):
                    if rect.collidepoint(mx, my):
                        selected_option = i

            elif game_state == "level_select":
                for lvl, rect in get_level_rows().items():
                    if rect.collidepoint(mx, my):
                        selected_level = lvl

        # KLIK MIŠEM
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if game_state == "main_menu":
                play_rect, levels_rect, exit_rect = get_main_menu_buttons()

                if play_rect.collidepoint(mx, my):
                    current_level = min(unlocked_levels, len(LEVELS))
                    score = 0
                    enemy_direction = 1
                    player, bullets, enemies, enemy_bullets, powerups, lives = start_level(current_level, 3)
                    game_state = "playing"

                elif levels_rect.collidepoint(mx, my):
                    selected_level = min(unlocked_levels, len(LEVELS))
                    game_state = "level_select"

                elif exit_rect.collidepoint(mx, my):
                    running = False

            elif game_state == "level_select":
                # klik na red levela prvo selektuje level
                for lvl, rect in get_level_rows().items():
                    if rect.collidepoint(mx, my):
                        selected_level = lvl
                        break

                buttons = get_level_select_buttons()

                if buttons["start"].collidepoint(mx, my):
                    if selected_level <= unlocked_levels:
                        current_level = selected_level
                        score = 0
                        enemy_direction = 1
                        player, bullets, enemies, enemy_bullets, powerups, lives = start_level(current_level, 3)
                        game_state = "playing"

                elif buttons["back"].collidepoint(mx, my):
                    game_state = "main_menu"

            elif game_state == "level_complete":
                buttons = get_level_complete_buttons()

                if "next" in buttons and buttons["next"].collidepoint(mx, my):
                    if current_level < len(LEVELS):
                        current_level += 1
                        if current_level > unlocked_levels:
                            unlocked_levels = current_level
                        selected_level = current_level
                        enemy_direction = 1
                        player, bullets, enemies, enemy_bullets, powerups, lives = start_level(current_level, 3)
                        game_state = "playing"

                elif buttons["restart"].collidepoint(mx, my):
                    score = 0
                    enemy_direction = 1
                    player, bullets, enemies, enemy_bullets, powerups, lives = start_level(current_level, 3)
                    game_state = "playing"

                elif buttons["menu"].collidepoint(mx, my):
                    selected_level = current_level
                    game_state = "main_menu"

            elif game_state == "game_over":
                buttons = get_game_over_buttons()

                if buttons["restart"].collidepoint(mx, my):
                    score = 0
                    enemy_direction = 1
                    player, bullets, enemies, enemy_bullets, powerups, lives = start_level(current_level, 3)
                    game_state = "playing"

                elif buttons["menu"].collidepoint(mx, my):
                    selected_level = current_level
                    game_state = "main_menu"

        # TASTATURA OSTAJE SAMO ZA IGRANJE I KAO REZERVA
        if event.type == pygame.KEYDOWN:
            if game_state == "playing":
                if event.key == pygame.K_SPACE:
                    current_time = pygame.time.get_ticks()

                    if current_time - last_shot_time >= SHOOT_COOLDOWN:
                        last_shot_time = current_time
                        bullet_y = player.y

                        if player.weapon_level == 1:
                            bullet_x = player.x + player.image.get_width() // 2 - 3
                            bullets.append(Bullet(bullet_x, bullet_y))

                        elif player.weapon_level == 2:
                            center_x = player.x + player.image.get_width() // 2
                            bullets.append(Bullet(center_x - 8, bullet_y, dx=-2))
                            bullets.append(Bullet(center_x + 8, bullet_y, dx=2))

                        else:
                            center_x = player.x + player.image.get_width() // 2
                            bullets.append(Bullet(center_x - 10, bullet_y, dx=-3))
                            bullets.append(Bullet(center_x, bullet_y, dx=0))
                            bullets.append(Bullet(center_x + 10, bullet_y, dx=3))

                        shoot_sound.play()

            elif event.key == pygame.K_ESCAPE:
                if game_state == "level_select":
                    game_state = "main_menu"
                elif game_state in ["main_menu", "game_over"]:
                    running = False

    if game_state == "playing":
        config = LEVELS[current_level]

        keys = pygame.key.get_pressed()
        player.move(keys)
        player.update()

        for bullet in bullets:
            bullet.move()

        if enemies:
            should_step_down = False

            for enemy in enemies:
                next_x = enemy.x + enemy.speed * ENEMY_H_SPEED_MULTIPLIER * enemy_direction
                if next_x <= EDGE_MARGIN or next_x + enemy.width >= WIDTH - EDGE_MARGIN:
                    should_step_down = True
                    break

            if should_step_down:
                enemy_direction *= -1
                for enemy in enemies:
                    enemy.step_down(STEP_DOWN_AMOUNT)
            else:
                for enemy in enemies:
                    enemy.move(enemy_direction * ENEMY_H_SPEED_MULTIPLIER)

        if config["enemy_shooting"] and enemies:
            reference_enemy_count = 10
            scale = max(len(enemies), 1) / reference_enemy_count
            effective_shoot_chance = max(int(config["shoot_chance"] * scale), 80)

            for enemy in enemies:
                if len(enemy_bullets) >= MAX_ENEMY_BULLETS:
                    break

                if random.randint(1, effective_shoot_chance) == 1:
                    bullet_x = enemy.x + enemy.width // 2
                    bullet_y = enemy.y + enemy.height
                    enemy_bullets.append(EnemyBullet(bullet_x, bullet_y))

        for bullet in enemy_bullets:
            bullet.move()

        for powerup in powerups:
            powerup.move()

        bullets = [bullet for bullet in bullets if not bullet.is_off_screen()]
        enemy_bullets = [bullet for bullet in enemy_bullets if not bullet.is_off_screen(HEIGHT)]
        powerups = [powerup for powerup in powerups if not powerup.is_off_screen(HEIGHT)]

        enemy_bullets_to_remove = []

        for bullet in enemy_bullets:
            if bullet.rect.colliderect(player.rect):

                # Ako je štit aktivan - odbij metak
                if player.shield_active:
                    bullet.speed *= -1
                    bullet.y -= 10
                    continue

                enemy_bullets_to_remove.append(bullet)

                if not player.is_invincible():
                    lives -= 1
                    score = max(0, score - 5)

                    score_change = "-5"
                    score_change_time = pygame.time.get_ticks()
                    score_change_y = 58

                    player.take_hit()

                    if lives <= 0:
                        game_state = "game_over"

        for bullet in enemy_bullets_to_remove:
            if bullet in enemy_bullets:
                enemy_bullets.remove(bullet)

        for powerup in powerups[:]:
            if powerup.rect.colliderect(player.rect):
                powerup_sound.play()

                if powerup.power_type == "shield":
                    player.activate_shield()

                elif powerup.power_type == "weapon":
                    player.weapon_level = min(player.weapon_level + 1, 3)

                powerups.remove(powerup)

        for enemy in enemies[:]:
            if enemy.rect.colliderect(player.rect) and not player.is_invincible():
                enemies.remove(enemy)
                lives -= 1
                score = max(0, score - 5)

                score_change = "-5"
                score_change_time = pygame.time.get_ticks()
                score_change_y = 58

                old_shield_active = player.shield_active
                old_shield_end_time = player.shield_end_time
                old_weapon_level = player.weapon_level

                player = Player()
                player.shield_active = old_shield_active
                player.shield_end_time = old_shield_end_time
                player.weapon_level = old_weapon_level
                player.take_hit()

                enemy_bullets.clear()

                if lives <= 0:
                    game_state = "game_over"

        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullets_to_remove.append(bullet)

                    destroyed = enemy.hit()

                    if destroyed:
                        explosion_sound.play()
                        enemies_to_remove.append(enemy)
                        score += enemy.points
                        score_change = f"+{enemy.points}"
                        score_change_time = pygame.time.get_ticks()
                        score_change_y = 58

                        if config["weapon_upgrade"] and player.weapon_level < 3 and random.randint(1, 8) == 1:
                            powerups.append(
                                PowerUp(
                                    enemy.x + enemy.width // 2 - 14,
                                    enemy.y + enemy.height // 2 - 14,
                                    "weapon"
                                )
                            )

                        elif current_level >= 5 and random.randint(1, 12) == 1:
                            powerups.append(
                                PowerUp(
                                    enemy.x + enemy.width // 2 - 14,
                                    enemy.y + enemy.height // 2 - 14,
                                    "shield"
                                )
                            )

                    break

        for bullet in bullets_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)

        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)

        for enemy in enemies[:]:
            if enemy.y + enemy.height >= HEIGHT:
                enemies.remove(enemy)

        if len(enemies) == 0 and game_state == "playing":
            completed_levels.add(current_level)

            if current_level < len(LEVELS) and unlocked_levels < current_level + 1:
                unlocked_levels = current_level + 1

            game_state = "level_complete"

    screen.fill((0, 0, 0))
    screen.blit(bg, (bg_x, bg_y))
    screen.blit(overlay, (0, 0))

    # IZMJENA: dva odvojena stanja za meni umjesto jednog "menu"
    if game_state == "main_menu":
        draw_main_menu(screen, selected_option, unlocked_levels, completed_levels)

    elif game_state == "level_select":
        draw_level_select(screen, selected_level, unlocked_levels, completed_levels)

    elif game_state == "playing":
        player.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

        for bullet in enemy_bullets:
            bullet.draw(screen)

        for powerup in powerups:
            powerup.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        draw_hud(screen, score, current_level, lives, player.shield_active, player.weapon_level)

        if pygame.time.get_ticks() - score_change_time < 1000 and score_change:
            font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 18)
            color = (80, 255, 120) if score_change.startswith("+") else (255, 70, 70)

            text = font.render(score_change, True, color)

            screen.blit(text, (62, score_change_y))

            score_change_y -= 0.25

    elif game_state == "level_complete":
        draw_hud(screen, score, current_level, lives, player.shield_active, player.weapon_level)
        draw_level_complete_menu(screen, current_level, unlocked_levels)

    elif game_state == "game_over":
        draw_hud(screen, score, current_level, lives, player.shield_active, player.weapon_level)
        draw_game_over_menu(screen, current_level)

    pygame.display.flip()

pygame.quit()