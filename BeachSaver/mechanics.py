import random, math
import pygame
from const import *
from objects import Obstacle, ScoreText

class GameMechanics:
    def __init__(self, player, font):
        self.player = player
        self.obstacles = []
        self.score_texts = []
        self.score = 0
        self.font = font
        self.spawn_timer = 0
        self.next_spawn = random.randint(OBSTACLE_SPACING_MIN, OBSTACLE_SPACING_MAX)

        # nuvens simples
        self.clouds = []
        for _ in range(5):
            self.clouds.append({
                "x": random.randint(0, wdt),
                "y": random.randint(20, hgt//2),
                "speed": random.uniform(0.2, 0.6),
                "size": random.randint(40, 80)
            })
        self.cloud_surface = pygame.Surface((wdt, hgt), pygame.SRCALPHA)

    def update(self, dt):
        self.spawn_timer += 4
        if self.spawn_timer > self.next_spawn:
            self.obstacles.append(Obstacle())
            self.spawn_timer = 0
            self.next_spawn = random.randint(OBSTACLE_SPACING_MIN, OBSTACLE_SPACING_MAX)

        self.player.update()

        for obs in self.obstacles[:]:
            obs.update()
            if not obs.passed:
                if self.player.rect.right > obs.rect.left and self.player.rect.left < obs.rect.right:
                    if self.player.y + 48 < obs.y:
                        self.score += POINTS_PASS_OVER
                        self.score_texts.append(ScoreText(self.player.x, self.player.y-20,
                                                          f"+{POINTS_PASS_OVER}", self.font))
                        obs.passed = True

            player_hitbox = pygame.Rect(int(self.player.x + 16), int(self.player.y + 32), 32, 32)
            if player_hitbox.colliderect(obs.rect) and not obs.passed:
                self.score += POINTS_COLLISION
                self.score_texts.append(ScoreText(self.player.x, self.player.y-20,
                                                  f"+{POINTS_COLLISION}", self.font))
                self.obstacles.remove(obs)

            if obs.x + obs.rect.width < 0:
                self.obstacles.remove(obs)

        for text in self.score_texts[:]:
            text.update()
            if text.alpha <= 0:
                self.score_texts.remove(text)

        for cloud in self.clouds:
            cloud["x"] += cloud["speed"]
            if cloud["x"] > wdt:
                cloud["x"] = -cloud["size"]
                cloud["y"] = random.randint(20, hgt//2)
                cloud["speed"] = random.uniform(0.2, 0.6)
                cloud["size"] = random.randint(40, 80)

    def draw(self, surface):
        # fundo degradê
        for y in range(hgt):
            factor = y / hgt
            r = int(50 * (1 - factor))
            g = int(70 * (1 - factor) + 50 * factor)
            b = int(160 * (1 - factor) + 170 * factor)
            pygame.draw.line(surface, (r, g, b), (0, y), (wdt, y))

        # nuvens
        self.cloud_surface.fill((0,0,0,0))
        for cloud in self.clouds:
            pygame.draw.ellipse(self.cloud_surface, (255,255,255,120),
                                (cloud["x"], cloud["y"], cloud["size"], cloud["size"]//2))
        surface.blit(self.cloud_surface, (0,0))

        # onda simples
        wave_height = 16
        wave_length = 64
        offset = pygame.time.get_ticks()/200
        for x in range(0, wdt, 2):
            y = hgt*0.75 + math.sin((x/wave_length)+offset)*wave_height
            pygame.draw.line(surface, ONDA, (x,y), (x,hgt))

        # player
        player_wave_y = hgt*0.75 + math.sin((self.player.x/wave_length)+offset)*wave_height
        self.player.update(wave_y=player_wave_y)
        self.player.draw(surface)

        # obstáculos e textos
        for obs in self.obstacles:
            obs.draw(surface)
        for text in self.score_texts:
            text.draw(surface)

        score_surface = self.font.render(f"SCORE: {self.score}", True, (255,255,0))
        surface.blit(score_surface, (10,10))
