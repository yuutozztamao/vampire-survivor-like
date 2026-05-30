import pygame

from settings import WIDTH, HEIGHT
from systems.drawing import *


class Player:

    draw_radius = 35
    images = []

    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.hit_radius = 30
        self.face = 0
        self.speed = 5
        self.max_health = 100
        self.health = self.max_health
        self.attack_rate = 1.0
        self.exp = 0
        self.lv = 0
        self.invincible_timer = 0

    @property
    def draw_x(self):
        return self.x - self.draw_radius

    @property
    def draw_y(self):
        return self.y - self.draw_radius

    def update(self, context):
        self.invincible_timer = max(self.invincible_timer - 1, 0)
        self.move(context.keys)

    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
            self.face = 0

        if keys[pygame.K_s]:
            self.y += self.speed
            self.face = 1

        if keys[pygame.K_a]:
            self.x -= self.speed
            self.face = 2

        if keys[pygame.K_d]:
            self.x += self.speed
            self.face = 3

        # 画面外に出ないようにする
        self.x = max(self.x, self.draw_radius)

        self.x = min(self.x, WIDTH - self.draw_radius)

        self.y = max(self.y, self.draw_radius)

        self.y = min(self.y, HEIGHT - self.draw_radius)

    def draw(self, screen):

        if self.invincible_timer > 0 and self.invincible_timer % 6 > 4:
            white_img = self.images[0].copy()
            white_img.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)
            screen.blit(white_img, (self.draw_x, self.draw_y))
        else:
            screen.blit(self.images[0], (self.draw_x, self.draw_y))

        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        length = 80
        value = self.health
        max_value = self.max_health
        height = 7
        x = self.x - length / 2
        y = self.y + self.hit_radius
        back_color = (100, 100, 100)
        bar_color = (0, 255, 0)

        draw_bar(screen, length, value, max_value, height, x, y, back_color, bar_color)
