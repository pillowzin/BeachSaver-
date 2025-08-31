import pygame
from const import *
import random
import math
import os

pygame.mixer.init()
jump_sound = pygame.mixer.Sound("sounds/jump.mp3")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.vel_y = 0
        self.on_ground = True

        # carregar spritesheet
        self.spritesheet = pygame.image.load("sprites/player.png").convert_alpha()
        self.frames = [self.spritesheet.subsurface((i*16, 0), (16,16)) for i in range(2)]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.rect.topleft = (self.x, self.y)

        # rotação 360
        self.rotation = 0
        self.rotating = False
        self.rotation_remaining = 0
        self.last_jump_time = 0

    def jump(self):
        
        now = pygame.time.get_ticks()
        # double-tap rápido inicia 360
        if now - self.last_jump_time < 300 and not self.on_ground:
            if not self.rotating:
                self.rotating = True
                self.rotation_remaining = 360
        self.last_jump_time = now

        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            jump_sound.play(loops=0)

    def update(self, wave_y=None):
        # animação de frames
        self.current_frame += 0.01
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

        # física do pulo
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED
        self.y += self.vel_y

        # chão da onda
        if wave_y is not None:
            ground_y = wave_y - 16
        else:
            ground_y = hgt*0.75 - 16

        if self.y >= ground_y:
            self.y = ground_y
            self.vel_y = 0
            self.on_ground = True
            self.rotating = False
            self.rotation = 0

        # animar rotação
        if self.rotating:
            rot_speed = 20
            step = min(rot_speed, self.rotation_remaining)
            self.rotation += step
            self.rotation_remaining -= step
            if self.rotation_remaining <= 0:
                self.rotating = False
                self.rotation = 0

        # escala e retângulo
        self.image = pygame.transform.scale(self.image, (64,64))
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = rotated_image.get_rect(center=(self.x+32, self.y+32))
        self.draw_image = rotated_image

    def draw(self, surface):
        # prancha
        board = pygame.image.load("sprites/board.png").convert_alpha()
        board = pygame.transform.scale(board, (64,16))
        surface.blit(board, (self.x, self.y+48))
        # player
        surface.blit(self.draw_image, self.rect.topleft)


class Obstacle(pygame.sprite.Sprite):
    SPRITE_FILES = ["Tshirt.png","Plastic.png","Glass.png"]

    def __init__(self, x=None):
        super().__init__()
        self.lives = 5
        self.x = x if x is not None else wdt
        self.base_y = hgt*0.75 - 32 + random.uniform(-10,10)
        self.y = self.base_y

		#carregar imagem
        sprite_file = random.choice(self.SPRITE_FILES)
        path = os.path.join("sprites", sprite_file)
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(topleft=(self.x, self.base_y))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.spawn_time = pygame.time.get_ticks()
        self.passed = False
        self.speed = 2 + random.random()*1.5




    def update(self):
        self.x -= self.speed
        t = pygame.time.get_ticks() - self.spawn_time
        self.y = self.base_y + math.sin(t/300)*5
        self.rect.topleft = (self.x, self.y)


    def draw(self, surface):
        surface.blit(self.image, self.rect)


class ScoreText:
    def __init__(self, x, y, text, font, color=(255,255,0)):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.alpha = 255

    def update(self):
        self.y -= 1
        self.alpha -= 5
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surface):
        img = self.font.render(self.text, True, self.color)
        img.set_alpha(self.alpha)
        surface.blit(img, (self.x, self.y))

