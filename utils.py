import pygame

def draw_glow_rect(screen, rect, color, glow_size=8, border_radius=10):
    for i in range(glow_size, 0, -1):
        glow_rect = pygame.Rect(
            rect.x - i,
            rect.y - i,
            rect.width + i * 2,
            rect.height + i * 2
        )
        s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            s,
            (*color, int(30 / i)),
            (0, 0, glow_rect.width, glow_rect.height),
            border_radius=border_radius
        )
        screen.blit(s, glow_rect.topleft)

    pygame.draw.rect(screen, color, rect, 2, border_radius=border_radius)


def draw_glow_text(screen, text, font, x, y, color):
    for i in range(3, 0, -1):
        glow = font.render(text, True, color)
        screen.blit(glow, (x - i, y))
        screen.blit(glow, (x + i, y))
        screen.blit(glow, (x, y - i))
        screen.blit(glow, (x, y + i))

    main = font.render(text, True, (255, 255, 255))
    screen.blit(main, (x, y))