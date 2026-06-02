import pygame
import random
import math

from settings import WIDTH
from systems.ui import draw_bar
from utils import is_in_camera
from gem import Gem
from enemy_bullet import EnemyBullet


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

        self.frozen_timer = 0
        self.frozen_rate = 0.5

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

        current_speed = self.speed
        if self.frozen_timer > 0:
            self.frozen_timer -= 1
            current_speed = self.speed * self.frozen_rate

        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.hypot(dx, dy)

        if distance != 0:
            self.x += dx / distance * current_speed
            self.y += dy / distance * current_speed

    def take_damage(self, context, base_attack_power):
        # 敵ダメージ
        real_damage = int(base_attack_power * context.player.attack_rate)
        self.health -= real_damage

        # ダメージ文字
        context.damage_texts.append(
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
            context.gems.append(new_gem)

            if isinstance(self, SlimeZombie) and self.split_count > 0:

                for i in range(2):

                    new_slime = SlimeZombie(
                        id=context.next_enemy_id,
                        x=self.x + random.randint(-30, 30),
                        y=self.y + random.randint(-30, 30),
                        size_rate=self.size_rate * 0.7,
                        split_count=self.split_count - 1,
                    )

                    context.enemies.append(new_slime)
                    context.next_enemy_id += 1

            context.enemies.remove(self)

    def draw(self, screen, context):

        cx = context.camera_x
        cy = context.camera_y

        if self.hit_effect_timer % 2 > 0:
            white_img = self.images[self.image_index].copy()
            white_img.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)
            screen.blit(
                white_img,
                (self.draw_x - cx, self.draw_y - cy),
            )
        else:
            screen.blit(
                self.images[self.image_index],
                (self.draw_x - cx, self.draw_y - cy),
            )

        self.draw_health_bar(screen, context)

    def draw_health_bar(self, screen, context):

        cx = context.camera_x
        cy = context.camera_y

        if self.health_bar_timer <= 0:
            return

        height = 7
        back_color = (100, 100, 100)
        bar_color = (0, 255, 0)

        length = self.hit_radius + 10
        value = self.health
        max_value = self.max_health

        x = self.x - length / 2 - cx
        y = self.y + self.draw_radius - cy

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


class ShooterZombie(Enemy):

    images = []
    bullet_images = []

    hit_radius = 40
    draw_radius = 40
    speed = 0.8
    max_health = 20
    attack_power = 50
    exp = 15
    bullet_hit_radius = 30
    bullet_draw_radius = 30
    bullet_speed = 2.5

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
        self.shoot_timer = 0
        self.shoot_cycle = 120

    def update(self, context):

        super().update(context)

        self.shoot_timer += 1

        if self.shoot_timer < self.shoot_cycle:
            return

        if not is_in_camera(
            self.x,
            self.y,
            context,
            margin=100,
        ):
            return

        player = context.player

        new_bullet = EnemyBullet(
            x=self.x,
            y=self.y,
            target_x=player.x,
            target_y=player.y,
            attack_power=self.attack_power,
            images=self.bullet_images,
            hit_radius=self.bullet_hit_radius,
            draw_radius=self.bullet_draw_radius,
            speed=self.bullet_speed,
        )

        context.enemy_bullets.append(new_bullet)

        self.shoot_timer = 0

    def move(self, player):

        current_speed = self.speed

        if self.frozen_timer > 0:
            self.frozen_timer -= 1
            current_speed = self.speed * self.frozen_rate

        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.hypot(dx, dy)

        if distance == 0:
            return

        # 理想距離
        target_distance = 250

        # 遠い → 接近
        if distance > target_distance + 20:

            self.x += dx / distance * current_speed
            self.y += dy / distance * current_speed

        # 近い → 後退
        elif distance < target_distance - 20:

            self.x -= dx / distance * current_speed
            self.y -= dy / distance * current_speed


class BoarZombie(Enemy):

    images = []

    hit_radius = 60
    draw_radius = 60

    speed = 4

    max_health = 40

    attack_power = 40

    exp = 15

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

        self.direction = 1

    def move(self, player):

        current_speed = self.speed

        if self.frozen_timer > 0:

            self.frozen_timer -= 1

            current_speed *= self.frozen_rate

        self.x += self.direction * current_speed

        # プレイヤーを中心にした画面の左端・右端
        left_limit = player.x - WIDTH / 2
        right_limit = player.x + WIDTH / 2

        if self.x < left_limit:
            self.direction = 1

        elif self.x > right_limit:
            self.direction = -1


class SlimeZombie(Enemy):

    images = []

    hit_radius = 100
    draw_radius = 100

    speed = 0.8

    max_health = 40

    attack_power = 10

    exp = 20

    def __init__(
        self,
        id,
        x,
        y,
        size_rate=1.0,
        split_count=2,
    ):

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
        self.size_rate = size_rate
        self.split_count = split_count

        if size_rate != 1.0:

            self.images = []

            for image in type(self).images:

                width = int(image.get_width() * size_rate)
                height = int(image.get_height() * size_rate)

                self.images.append(
                    pygame.transform.scale(
                        image,
                        (width, height),
                    )
                )

        self.hit_radius *= size_rate
        self.draw_radius *= size_rate

        self.max_health = int(self.max_health * size_rate)
        self.health = self.max_health

        self.image_index = 0


class BomberZombie(Enemy):

    images = []

    hit_radius = 35
    draw_radius = 35

    speed = 1.2

    max_health = 30

    attack_power = 10
    explosion_attack_power = 50

    exp = 20

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

        self.explode_distance = 150
        self.explode_timer = 0
        self.explode_cycle = 90
        self.exploded = False
        self.explosion_radius = 150

    def update(self, context):

        super().update(context)

        player = context.player

        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)

        if distance < self.explode_distance:
            self.explode_timer += 1
        else:
            self.explode_timer = 0

        if self.explode_timer >= self.explode_cycle:

            if distance < self.explosion_radius:
                player.take_damage(
                    context,
                    self.explosion_attack_power,
                )

            context.explosions.append(
                {
                    "x": self.x,
                    "y": self.y,
                    "radius": self.explosion_radius,
                    "timer": 20,
                }
            )
            context.enemies.remove(self)

    def draw(self, screen, context):

        ratio = self.explode_timer / self.explode_cycle

        scale = 1 + ratio * 0.2

        image = self.images[self.image_index]

        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)

        scaled_image = pygame.transform.scale(
            image,
            (width, height),
        )

        red_image = scaled_image.copy()

        red_power = int(120 * ratio)

        red_image.fill(
            (red_power, 0, 0),
            special_flags=pygame.BLEND_RGB_ADD,
        )

        cx = context.camera_x
        cy = context.camera_y

        screen.blit(
            red_image,
            (
                self.x - width / 2 - cx,
                self.y - height / 2 - cy,
            ),
        )

        if self.explode_timer > 0:

            pygame.draw.circle(
                screen,
                (255, 120, 120),
                (
                    self.x - cx,
                    self.y - cy,
                ),
                self.explosion_radius,
                2,
            )

        self.draw_health_bar(screen, context)
