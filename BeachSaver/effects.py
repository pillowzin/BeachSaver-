import pygame
from const import wdt, hgt

def fade_in(surface, speed=5):
    fade = pygame.Surface((wdt, hgt))
    fade.fill((0,0,0))
    for alpha in range(255, -1, -speed):
        fade.set_alpha(alpha)
        surface.fill((0,0,0))  # opcional, se quiser fundo limpo
        pygame.display.flip()
        surface.blit(fade, (0,0))
        pygame.time.delay(5)  # controla a velocidade do fade

def fade_out(surface, speed=5):
    fade = pygame.Surface((wdt, hgt))
    fade.fill((0,0,0))
    for alpha in range(0, 256, speed):
        fade.set_alpha(alpha)
        pygame.display.flip()
        surface.blit(fade, (0,0))
        pygame.time.delay(5)