import pygame
import random
import math

from systems.drawing import *
from gem import *


class Enemy:

    def __init__(
        self,
        id,
        x,
        y,
        hit_radius,
        draw_radius,
        speed,
        max_health,
        attack_power,
        exp,
        images,
    ):
        self.id = id
        self.x = x
        self.y = y
        self.hit_radius = hit_radius
        self.draw_radius = draw_radius
        self.speed = speed
        self.max_health = max_health
        self.health = max_health
        self.attack_power = attack_power
        self.exp = exp
        self.images = images
        self.health_bar_timer = 0
        self.hit_effect_timer = 0
        self.image_index = 0

    @property
    def draw_x(self):
        return self.x - self.draw_radius

    @property
    def draw_y(self):
        return self.y - self.draw_radius

    def update(self, context):
        self.move(context.player)
        self.hit_effect_timer = max(self.hit_effect_timer - 1, 0)
        self.health_bar_timer = max(self.health_bar_timer - 1, 0)

    def move(self, player):

        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.hypot(dx, dy)

        if distance != 0:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

    def take_damage(self, player, enemies, base_attack_power, damage_texts, gems):
        # 敵ダメージ
        real_damage = int(base_attack_power * player.attack_rate)
        self.health -= real_damage

        # ダメージ文字
        damage_texts.append(
            {
                "x": random.uniform(
                    self.x - self.draw_radius / 2,
                    self.x + self.draw_radius / 2,
                ),
                "y": random.uniform(
                    self.y - self.draw_radius / 2,
                    self.y + self.draw_radius / 2,
                ),
                "damage": real_damage,
                "timer": 30,
            }
        )

        # 点滅タイマー、HPバー表示タイマー
        self.hit_effect_timer = 5
        self.health_bar_timer = 35

        # 敵死亡
        if self.health <= 0:

            x = self.x
            y = self.y

            new_gem = Gem(x, y, self.exp)
            gems.append(new_gem)

            enemies.remove(self)

    def draw(self, screen):

        if self.hit_effect_timer % 2 > 0:
            white_img = self.images[self.image_index].copy()
            white_img.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)
            screen.blit(white_img, (self.draw_x, self.draw_y))
        else:
            screen.blit(self.images[self.image_index], (self.draw_x, self.draw_y))

        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        if self.health_bar_timer <= 0:
            return

        height = 7
        back_color = (100, 100, 100)
        bar_color = (0, 255, 0)

        length = self.hit_radius + 10
        value = self.health
        max_value = self.max_health
        x = self.x - length / 2
        y = self.y + self.draw_radius

        draw_bar(screen, length, value, max_value, height, x, y, back_color, bar_color)


class Zombie(Enemy):

    images = []
    hit_radius = 30
    draw_radius = 30
    speed = 1
    max_health = 30
    attack_power = 10
    exp = 10

    def __init__(self, id, x, y):

        cls = type(self)

        super().__init__(
            id=id,
            x=x,
            y=y,
            hit_radius=cls.hit_radius,
            draw_radius=cls.draw_radius,
            speed=cls.speed,
            max_health=cls.max_health,
            attack_power=cls.attack_power,
            exp=cls.exp,
            images=cls.images,
        )


class MuscleZombie(Enemy):

    images = []
    hit_radius = 45
    draw_radius = 45
    speed = 1.5
    max_health = 40
    attack_power = 10
    exp = 10

    def __init__(self, id, x, y):

        cls = type(self)

        super().__init__(
            id=id,
            x=x,
            y=y,
            hit_radius=cls.hit_radius,
            draw_radius=cls.draw_radius,
            speed=cls.speed,
            max_health=cls.max_health,
            attack_power=cls.attack_power,
            exp=cls.exp,
            images=cls.images,
        )
