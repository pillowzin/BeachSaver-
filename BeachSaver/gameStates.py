import pygame
import random
import math
from const import *

class GameState:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

class Menu(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
        self.particles = [(random.randint(0, wdt), random.randint(0, hgt//2)) for _ in range(30)]

    def update(self, dt):
        for i, (x, y) in enumerate(self.particles):
            y += dt * 0.05
            if y > hgt//2:
                y = 0
                x = random.randint(0, wdt)
            self.particles[i] = (x, y)

    def draw(self, surface):
        # fundo degradê limpo azul-arroxeado
        for y in range(hgt):
            factor = y / hgt
            r = int(50 * (1 - factor))
            g = int(70 * (1 - factor) + 50 * factor)
            b = int(160 * (1 - factor) + 190 * factor)
            pygame.draw.line(surface, (r, g, b), (0, y), (wdt, y))

        # partículas simples
        for x, y in self.particles:
            pygame.draw.circle(surface, (255, 220, 50), (int(x), int(y)), 2)

        # texto central
        text = self.font.render(f"Objetivo: Coletar {TARGET_SCORE} pontos", True, (245, 245, 220))
        surface.blit(text, (wdt//2 - text.get_width()//2, hgt//2 - text.get_height()//2))

        pygame.display.flip()

class Concluido(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)

    def draw(self, surface):
        # fundo azul-arroxeado simples
        pulse = (math.sin(pygame.time.get_ticks()/500) + 1)/2
        r = int(50 + 60 * pulse)
        g = int(70 + 50 * (1 - pulse))
        b = int(150 + 40 * pulse)
        surface.fill((r, g, b))

        # texto central
        text = self.font.render("Jogo Concluído!", True, (245, 245, 220))
        surface.blit(text, (wdt//2 - text.get_width()//2, hgt//2 - text.get_height()//2))

        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12)
        text = self.font.render("Aperte R para jogar denovo", True, (245, 245, 220))
        surface.blit(text, (wdt//2 - text.get_width()//2, hgt//2 - text.get_height()//2+60))

        pygame.display.flip()
