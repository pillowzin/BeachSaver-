import pygame
from const import *
from objects import Player
from gameMechanics import GameMechanics
from gameStates import Menu, Concluido, Morte
import random

pygame.init()
screen = pygame.display.set_mode((wdt, hgt))
pygame.display.set_caption("Beach Saver!")
clock = pygame.time.Clock()

font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 16)
player = Player(wdt//4, hgt*0.75 - 16)
mechanics = GameMechanics(player, font)

state = Menu(None)
running = True
game_started = False

while running:
    dt = clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_started:
                game_started = True
                state = mechanics
            if event.key == pygame.K_r:
                # reset player
                player.x = wdt//4
                player.y = hgt*0.75 - 16
                player.vel_y = 0
                player.on_ground = True
                player.rotating = False
                player.rotation = 0
                player.lives = 3  # ou o valor inicial

                # reset mecânica
                mechanics.obstacles.clear()
                mechanics.obstacle_group.empty()  # limpa sprites
                mechanics.score_texts.clear()
                mechanics.score = 0
                mechanics.spawn_timer = 0
                mechanics.next_spawn = random.randint(OBSTACLE_SPACING_MIN, OBSTACLE_SPACING_MAX)

                # reset nuvens
                for cloud in mechanics.clouds:
                    cloud["x"] = random.randint(0, wdt)
                    cloud["y"] = random.randint(20, hgt//2)
                    cloud["speed"] = random.uniform(0.2, 0.6)
                    cloud["size"] = random.randint(40, 80)

                game_started = True
                state = mechanics

    keys = pygame.key.get_pressed()
    if game_started:
        if keys[pygame.K_SPACE]:
            player.jump()
        if not player.on_ground:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.x -= 3
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.x += 3

        mechanics.update(dt)
        mechanics.draw(screen)

        if mechanics.score >= TARGET_SCORE:
            state = Concluido(None)
            game_started = False
            state.draw(screen)
    else:
        state.draw(screen)

    pygame.display.flip()

pygame.quit()
