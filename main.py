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
from menu import draw_menu, draw_level_complete_menu, draw_game_over_menu

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

bg = pygame.image.load("assets/images/bg2.jpg").convert()
bg_rect = bg.get_rect()
scale_ratio = min(WIDTH / bg_rect.width, HEIGHT / bg_rect.height)

new_width = int(bg_rect.width * scale_ratio)
new_height = int(bg_rect.height * scale_ratio)

bg = pygame.transform.smoothscale(bg, (new_width, new_height))
bg_x = (WIDTH - new_width) // 2
bg_y = (HEIGHT - new_height) // 2

overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.set_alpha(25)
overlay.fill((10, 20, 50))


def start_level(level):
    player = Player()
    bullets = []
    enemies = create_enemies(level)
    enemy_bullets = []
    powerups = []
    lives = 3
    return player, bullets, enemies, enemy_bullets, powerups, lives


current_level = 1
selected_level = 1
unlocked_levels = 1
completed_levels = set()

player, bullets, enemies, enemy_bullets, powerups, lives = start_level(current_level)
score = 0

game_state = "menu"
running = True


while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_UP:
                    selected_level -= 1
                    if selected_level < 1:
                        selected_level = len(LEVELS)

                elif event.key == pygame.K_DOWN:
                    selected_level += 1
                    if selected_level > len(LEVELS):
                        selected_level = 1

                elif event.key == pygame.K_RETURN:
                    if selected_level <= unlocked_levels:
                        current_level = selected_level
                        player, bullets, enemies, enemy_bullets, powerups, lives = start_level(current_level)
                        game_state = "playing"

                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif game_state == "playing":
                if event.key == pygame.K_SPACE:
                    bullet_y = player.y

                    if player.weapon_level == 1:
                        bullet_x = player.x + player.image.get_width() // 2 - 3
                        bullets.append(Bullet(bullet_x, bullet_y))

                    elif player.weapon_level == 2:
                        center_x = player.x + player.image.get_width() // 2
                        bullets.append(Bullet(center_x - 14, bullet_y))
                        bullets.append(Bullet(center_x + 8, bullet_y))

                    else:
                        center_x = player.x + player.image.get_width() // 2
                        bullets.append(Bullet(center_x - 20, bullet_y))
                        bullets.append(Bullet(center_x - 3, bullet_y))
                        bullets.append(Bullet(center_x + 14, bullet_y))

            elif game_state == "level_complete":
                if event.key == pygame.K_n:
                    if current_level < len(LEVELS):
                        current_level += 1
                        if current_level > unlocked_levels:
                            unlocked_levels = current_level

                        selected_level = current_level
                        player, bullets, enemies, enemy_bullets, powerups, lives = start_level(current_level)
                        game_state = "playing"

                elif event.key == pygame.K_r:
                    player, bullets, enemies, enemy_bullets, powerups, lives = start_level(current_level)
                    game_state = "playing"

                elif event.key == pygame.K_m:
                    selected_level = current_level
                    game_state = "menu"

            elif game_state == "game_over":
                if event.key == pygame.K_r:
                    player, bullets, enemies, enemy_bullets, powerups, lives = start_level(current_level)
                    game_state = "playing"

                elif event.key == pygame.K_m:
                    selected_level = current_level
                    game_state = "menu"

    if game_state == "playing":
        config = LEVELS[current_level]

        keys = pygame.key.get_pressed()
        player.move(keys)
        player.update()

        for bullet in bullets:
            bullet.move()

        for enemy in enemies:
            enemy.move()

        if config["enemy_shooting"]:
            for enemy in enemies:
                if random.randint(1, config["shoot_chance"]) == 1:
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
                enemy_bullets_to_remove.append(bullet)

                if not player.shield_active:
                    lives -= 1
                    if lives <= 0:
                        game_state = "game_over"

        for bullet in enemy_bullets_to_remove:
            if bullet in enemy_bullets:
                enemy_bullets.remove(bullet)

        for powerup in powerups[:]:
            if powerup.rect.colliderect(player.rect):
                if powerup.power_type == "shield":
                    player.activate_shield()
                elif powerup.power_type == "weapon":
                    player.weapon_level = min(player.weapon_level + 1, 3)

                powerups.remove(powerup)

        for enemy in enemies:
            if enemy.rect.colliderect(player.rect):
                game_state = "game_over"

        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullets_to_remove.append(bullet)

                    if enemy.enemy_type == "forbidden":
                        game_state = "game_over"
                        break

                    destroyed = enemy.hit()

                    if destroyed:
                        enemies_to_remove.append(enemy)
                        score += enemy.points

                        if enemy.enemy_type == "weapon":
                            powerups.append(
                                PowerUp(
                                    enemy.x + enemy.width // 2 - 14,
                                    enemy.y + enemy.height // 2 - 14,
                                    "weapon"
                                )
                            )

                        elif enemy.enemy_type == "shield":
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
                lives -= 1
                if lives <= 0:
                    game_state = "game_over"

        if len(enemies) == 0 and game_state == "playing":
            completed_levels.add(current_level)

            if current_level < len(LEVELS) and unlocked_levels < current_level + 1:
                unlocked_levels = current_level + 1

            game_state = "level_complete"

    screen.fill((0, 0, 0))
    screen.blit(bg, (bg_x, bg_y))
    screen.blit(overlay, (0, 0))

    if game_state == "menu":
        draw_menu(screen, selected_level, unlocked_levels, completed_levels)

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

    elif game_state == "level_complete":
        draw_hud(screen, score, current_level, lives, player.shield_active, player.weapon_level)
        draw_level_complete_menu(screen, current_level, unlocked_levels)

    elif game_state == "game_over":
        draw_hud(screen, score, current_level, lives, player.shield_active, player.weapon_level)
        draw_game_over_menu(screen, current_level)

    pygame.display.flip()

pygame.quit()