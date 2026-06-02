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
        self.pickup_radius = 100
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
        self.move(context)

    def move(self, context):

        keys = context.keys

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

    def take_damage(self, context, attack_power):

        if self.invincible_timer > 0:
            return False

        self.health -= attack_power

        self.invincible_timer = 30

        if self.health <= 0:
            context.game_over = True

        return True

    def draw(self, screen, context):

        cx = context.camera_x
        cy = context.camera_y

        if self.invincible_timer > 0 and self.invincible_timer % 6 > 4:
            white_img = self.images[0].copy()
            white_img.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)
            screen.blit(white_img, (self.draw_x - cx, self.draw_y - cy))
        else:
            screen.blit(self.images[0], (self.draw_x - cx, self.draw_y - cy))

        self.draw_health_bar(screen, context)

    def draw_health_bar(self, screen, context):

        cx = context.camera_x
        cy = context.camera_y

        length = 80
        value = self.health
        max_value = self.max_health
        height = 7

        x = self.x - length / 2 - cx
        y = self.y + self.hit_radius - cy

        back_color = (100, 100, 100)
        bar_color = (0, 255, 0)

        draw_bar(screen, length, value, max_value, height, x, y, back_color, bar_color)
