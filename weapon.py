import random
import math

from bullet import *


class Weapon:

    def __init__(self, name, cycle, attack_power, level_data):

        self.name = name
        self.cycle = cycle
        self.timer = 0
        self.attack_power = attack_power
        self.level = 1
        self.level_data = level_data
        self.unlocked = False

    def level_up(self, weapons, level_up_list):

        if not self.unlocked:
            weapons.append(self)
            self.unlocked = True
            return

        # 最大レベル
        if self.level >= len(self.level_data) + 1:
            level_up_list.discard(self)
            return False

        level_param = self.level_data[self.level - 1]

        for param, value in level_param.items():

            setattr(self, param, getattr(self, param) + value)

        self.level += 1

        return True


class ShootingWeapon(Weapon):

    def __init__(
        self,
        name,
        cycle,
        attack_power,
        bullet_speed,
        bullet_hit_radius,
        bullet_draw_radius,
        through,
        level_data,
    ):

        super().__init__(name, cycle, attack_power, level_data)

        self.bullet_speed = bullet_speed
        self.bullet_hit_radius = bullet_hit_radius
        self.bullet_draw_radius = bullet_draw_radius
        self.through = through
        self.level_data = level_data

    def update(self, context):

        self.timer += 1

        if self.timer > self.cycle:

            self.shoot(context.player, context.bullets, context.enemies)

            self.timer = 0


class DamageAreaWeapon(Weapon):

    def __init__(self, name, cycle, attack_power, level_data):

        super().__init__(name, cycle, attack_power, level_data)

        self.level_data = level_data
        self.image_index = 0

    def update(self, context):

        self.timer += 1

        if self.timer > self.cycle:
            self.attack(
                context.player, context.enemies, context.damage_texts, context.gems
            )
            self.timer = 0


class NormalWeapon(ShootingWeapon):

    name = "NORMAL SHOT"

    cycle = 40
    attack_power = 10
    bullet_speed = 10
    bullet_hit_radius = 20
    bullet_draw_radius = 20
    through = False
    bullet_images = []

    level_data = [
        {"cycle": -5},
        {"attack_power": 5},
    ]

    def __init__(self):

        cls = type(self)

        super().__init__(
            name=cls.name,
            cycle=cls.cycle,
            attack_power=cls.attack_power,
            bullet_speed=cls.bullet_speed,
            bullet_hit_radius=cls.bullet_hit_radius,
            bullet_draw_radius=cls.bullet_draw_radius,
            through=cls.through,
            level_data=cls.level_data,
        )

    def shoot(self, player, bullets, enemies):

        x_speed = 0
        y_speed = 0

        if player.face == 0:
            y_speed = -self.bullet_speed

        if player.face == 1:
            y_speed = self.bullet_speed

        if player.face == 2:
            x_speed = -self.bullet_speed

        if player.face == 3:
            x_speed = self.bullet_speed

        bullet = Bullet(
            x=player.x,
            y=player.y,
            x_speed=x_speed,
            y_speed=y_speed,
            hit_radius=self.bullet_hit_radius,
            draw_radius=self.bullet_draw_radius,
            attack_power=self.attack_power,
            through=self.through,
            images=self.bullet_images,
        )

        bullets.append(bullet)


class RandomWeapon(ShootingWeapon):

    name = "RANDOM SHOT"

    cycle = 20
    attack_power = 10

    bullet_speed = 10
    bullet_hit_radius = 20
    bullet_draw_radius = 20

    through = False
    bullet_images = []

    level_data = [
        {"cycle": -5},
        {"attack_power": 5},
    ]

    def __init__(self):

        cls = type(self)

        super().__init__(
            name=cls.name,
            cycle=cls.cycle,
            attack_power=cls.attack_power,
            bullet_speed=cls.bullet_speed,
            bullet_hit_radius=cls.bullet_hit_radius,
            bullet_draw_radius=cls.bullet_draw_radius,
            through=cls.through,
            level_data=cls.level_data,
        )

    def shoot(self, player, bullets, enemies):

        angle = random.randint(0, 360)

        x_speed = math.cos(math.radians(angle)) * self.bullet_speed
        y_speed = math.sin(math.radians(angle)) * self.bullet_speed

        bullet = Bullet(
            x=player.x,
            y=player.y,
            x_speed=x_speed,
            y_speed=y_speed,
            hit_radius=self.bullet_hit_radius,
            draw_radius=self.bullet_draw_radius,
            attack_power=self.attack_power,
            through=self.through,
            images=self.bullet_images,
        )

        bullets.append(bullet)


class RandomAimWeapon(ShootingWeapon):

    name = "RANDOM AIM SHOT"

    cycle = 60
    attack_power = 10

    bullet_speed = 5
    bullet_hit_radius = 30
    bullet_draw_radius = 30

    through = True
    bullet_images = []

    level_data = [
        {"cycle": -5},
        {"attack_power": 5},
    ]

    def __init__(self):

        cls = type(self)

        super().__init__(
            name=cls.name,
            cycle=cls.cycle,
            attack_power=cls.attack_power,
            bullet_speed=cls.bullet_speed,
            bullet_hit_radius=cls.bullet_hit_radius,
            bullet_draw_radius=cls.bullet_draw_radius,
            through=cls.through,
            level_data=cls.level_data,
        )

    def shoot(self, player, bullets, enemies):

        if not enemies:
            return

        enemy = random.choice(enemies)

        angle = math.atan2((enemy.y - player.y), (enemy.x - player.x))
        x_speed = self.bullet_speed * math.cos(angle)
        y_speed = self.bullet_speed * math.sin(angle)

        bullet = Bullet(
            x=player.x,
            y=player.y,
            x_speed=x_speed,
            y_speed=y_speed,
            hit_radius=self.bullet_hit_radius,
            draw_radius=self.bullet_draw_radius,
            attack_power=self.attack_power,
            through=self.through,
            images=self.bullet_images,
        )

        bullets.append(bullet)


class SurroundWeapon(DamageAreaWeapon):

    name = "SURROUND AREA"

    cycle = 20
    attack_power = 7

    outer_hit_radius = 200
    inner_hit_radius = 150
    images = []

    level_data = [
        {"cycle": -5},
        {"attack_power": 5},
    ]

    @property
    def draw_radius(self):

        return (self.outer_hit_radius - self.inner_hit_radius) / 2

    @classmethod
    def get_draw_radius(cls):

        return (cls.outer_hit_radius - cls.inner_hit_radius) / 2

    def __init__(self):

        cls = type(self)

        super().__init__(
            name=cls.name,
            cycle=cls.cycle,
            attack_power=cls.attack_power,
            level_data=cls.level_data,
        )
        self.outer_hit_radius = cls.outer_hit_radius
        self.inner_hit_radius = cls.inner_hit_radius
        self.rotation = 0
        self.image_index = 0

    # @property
    # def draw_radius(self):
    #    return (self.hit_radius - self.inner_hit_radius) / 2

    def update(self, context):

        super().update(context)

        self.rotation += 2

    def attack(self, player, enemies, damage_texts, gems):

        for enemy in enemies[:]:

            # 中心同士の距離
            dx = player.x - enemy.x
            dy = player.y - enemy.y

            distance = math.hypot(dx, dy)

            # 敵の半径
            enemy_hit_radius = enemy.hit_radius / 2

            # 円との接触判定
            if (
                distance + enemy_hit_radius > self.inner_hit_radius
                and distance - enemy_hit_radius < self.outer_hit_radius
            ):

                enemy.take_damage(
                    player, enemies, self.attack_power, damage_texts, gems
                )

    def draw(self, screen, player):

        saw_count = 6

        # 画像の軌道の半径
        orbit_radius = (self.outer_hit_radius + self.inner_hit_radius) / 2

        for i in range(saw_count):

            angle = (360 / saw_count * i) + self.rotation

            radian = math.radians(angle)

            x = player.x + math.cos(radian) * orbit_radius
            y = player.y + math.sin(radian) * orbit_radius

            draw_x = x - self.draw_radius
            draw_y = y - self.draw_radius

            screen.blit(self.images[self.image_index], (draw_x, draw_y))
