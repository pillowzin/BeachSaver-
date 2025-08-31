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

        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.obstacle_group = pygame.sprite.Group()

    def update(self, dt):
        # spawn de obstáculos
        self.spawn_timer += 4
        if self.spawn_timer > self.next_spawn:
            obs = Obstacle()
            self.obstacles.append(obs)
            self.obstacle_group.add(obs)
            self.spawn_timer = 0
            self.next_spawn = random.randint(OBSTACLE_SPACING_MIN, OBSTACLE_SPACING_MAX)

        # atualizar player
        self.player.update()

        # colisões: perde pontos ao colidir
        hits = pygame.sprite.spritecollide(self.player, self.obstacle_group, False)
        for obs in hits:
            if not obs.passed:
                # diminuir pontos ao colidir
                self.score += POINTS_COLLISION  # normalmente POINTS_COLLISION = -5
                self.score_texts.append(ScoreText(self.player.x, self.player.y-20,
                                                f"{POINTS_COLLISION}", self.font, color=(255,0,0)))
                obs.passed = True  # marca que já passou pra não repetir
        # pontos por passar por cima
        for obs in self.obstacles:
            if not obs.passed and self.player.x > obs.x + obs.rect.width:
                self.score += POINTS_PASS_OVER
                self.score_texts.append(ScoreText(self.player.x, self.player.y-20,
                                                  f"+{POINTS_PASS_OVER}", self.font, color=(255,255,0)))
                obs.passed = True

        # atualizar textos de pontuação
        for text in self.score_texts[:]:
            text.update()
            if text.alpha <= 0:
                self.score_texts.remove(text)

        # atualizar nuvens
        for cloud in self.clouds:
            cloud["x"] += cloud["speed"]
            if cloud["x"] > wdt:
                cloud["x"] = -cloud["size"]
                cloud["y"] = random.randint(20, hgt//2)
                cloud["speed"] = random.uniform(0.2, 0.6)
                cloud["size"] = random.randint(40, 80)

        # remover obstáculos fora da tela
        for obs in self.obstacles[:]:
            if obs.x + obs.rect.width < 0:
                self.obstacles.remove(obs)
                self.obstacle_group.remove(obs)

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

        # atualizar e desenhar obstáculos
        self.obstacle_group.update()
        self.obstacle_group.draw(surface)

        # desenhar pontuação
        for text in self.score_texts:
            text.draw(surface)

        score_surface = self.font.render(f"SCORE: {self.score}", True, (255,255,0))
        surface.blit(score_surface, (10,10))

        