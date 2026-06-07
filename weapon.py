import random
import math
from settings import WIDTH, HEIGHT

from systems.collision import damage_shields_in_circle
from systems.effect import add_lightning_effect
from bullet import Bullet
from mine import Mine
from hornet_nest import HornetNest
from utils import (
    enemy_knockback,
    get_direction_and_distance,
    get_closest_objects,
)

class Weapon:

    def __init__(self, name, cycle, attack_power, level_data):

        self.name = name
        self.cycle = cycle
        self.timer = 0
        self.attack_power = attack_power
        self.level = 1
        self.level_data = level_data

    @property
    def is_max_level(self):

        return self.level > len(self.level_data)

    @property
    def next_level_data(self):

        if self.is_max_level:
            return None

        return self.level_data[self.level - 1]

    def update(self, context):

        if self.is_ready():

            self.activate(context)

    def activate(self, context):

        raise NotImplementedError

    def level_up(self):

        if self.is_max_level:
            return False

        data = self.level_data[self.level - 1]

        for param, value in data.items():

            setattr(
                self,
                param,
                getattr(self, param) + value,
            )

        self.level += 1
        print(
            self.name,
            "Lv",
            self.level,
            "Cycle",
            self.cycle,
            "Attack",
            self.attack_power,
        )
        return True

    def is_ready(self):

        self.timer += 1

        if self.timer <= self.cycle:
            return False

        self.timer = 0

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
        self.shot_count = 2

    def activate(self, context):

        self.shoot(context)


class DamageAreaWeapon(Weapon):

    def __init__(self, name, cycle, attack_power, level_data):

        super().__init__(name, cycle, attack_power, level_data)

    def activate(self, context):

        self.attack(context)


class NormalWeapon(ShootingWeapon):

    weapon_id = "normal_weapon"
    name = "NORMAL SHOT"

    cycle = 60
    attack_power = 10
    bullet_speed = 10
    bullet_hit_radius = 20
    bullet_draw_radius = 20
    through = False
    bullet_images = []

    level_data = [
        {"cycle": -10, "attack_power": 5},
        {"cycle": -10, "attack_power": 15},
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

    def shoot(self, context):

        player = context.player
        bullets = context.bullets

        face_angle_map = {
            0: -90,  # 上
            1: 90,  # 下
            2: 180,  # 左
            3: 0,  # 右
        }

        base_angle = face_angle_map[player.face]

        for i in range(self.shot_count):

            angle = base_angle + 360 / self.shot_count * i

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


class RandomWeapon(ShootingWeapon):

    weapon_id = "random_weapon"
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
        {"shot_count": 1},
        {"shot_count": 1},
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

    def shoot(self, context):

        player = context.player
        bullets = context.bullets

        for _ in range(self.shot_count):

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

    weapon_id = "random_aim_weapon"
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
        {"shot_count": 1},
        {"shot_count": 1},
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

    def shoot(self, context):

        player = context.player
        bullets = context.bullets
        enemies = context.enemies

        if not enemies:
            return

        target_count = min(
            self.shot_count,
            len(enemies),
        )

        targets = random.sample(
            enemies,
            target_count,
        )

        for enemy in targets:

            angle = math.atan2(
                enemy.y - player.y,
                enemy.x - player.x,
            )

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


class FreezeWeapon(ShootingWeapon):

    weapon_id = "freeze_weapon"
    name = "FREEZE SHOT"

    cycle = 60
    attack_power = 5

    bullet_speed = 7
    bullet_hit_radius = 20
    bullet_draw_radius = 20

    through = False
    bullet_images = []

    level_data = [
        {"cycle": -5},
        {"attack_power": 5},
        {"shot_count": 1},
        {"shot_count": 1},
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

    def shoot(self, context):

        player = context.player
        bullets = context.bullets
        enemies = context.enemies

        if not enemies:
            return

        targets = get_closest_objects(
            player,
            enemies,
            self.shot_count,
        )

        for enemy in targets:

            angle = math.atan2(
                enemy.y - player.y,
                enemy.x - player.x,
            )

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
                freeze=True,
            )

            bullets.append(bullet)


class SurroundWeapon(DamageAreaWeapon):

    weapon_id = "surround_weapon"
    name = "SURROUND AREA"

    cycle = 20
    attack_power = 4

    outer_hit_radius = 200
    inner_hit_radius = 150
    knockback_power = 20
    knockback_rate = 0.3
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
        self.knockback_power = cls.knockback_power
        self.image_index = 0

    # @property
    # def draw_radius(self):
    #    return (self.hit_radius - self.inner_hit_radius) / 2

    def update(self, context):

        super().update(context)

        self.rotation += 2

    def attack(self, context):

        damage_shields_in_circle(
            context,
            context.player.x,
            context.player.y,
            self.outer_hit_radius,
            self.attack_power,
        )

        for enemy in context.enemies[:]:

            # 中心同士の距離
            _, _, distance = get_direction_and_distance(enemy, context.player)

            # 敵の半径
            enemy_hit_radius = enemy.hit_radius / 2

            # 円との接触判定
            if (
                distance + enemy_hit_radius > self.inner_hit_radius
                and distance - enemy_hit_radius < self.outer_hit_radius
            ):

                enemy.take_damage(context, self.attack_power)

                if random.random() < self.knockback_rate:

                    enemy_knockback(
                        enemy,
                        context.player,
                        self.knockback_power,
                    )

    def draw(self, screen, context):

        player = context.player
        cx = context.camera_x
        cy = context.camera_y

        saw_count = 6
        orbit_radius = (self.outer_hit_radius + self.inner_hit_radius) / 2

        for i in range(saw_count):

            angle = (360 / saw_count * i) + self.rotation
            radian = math.radians(angle)

            x = player.x + math.cos(radian) * orbit_radius
            y = player.y + math.sin(radian) * orbit_radius

            draw_x = x - self.draw_radius - cx
            draw_y = y - self.draw_radius - cy

            screen.blit(self.images[self.image_index], (draw_x, draw_y))


class ChainLightningWeapon(Weapon):

    weapon_id = "chain_lightning_weapon"

    name = "CHAIN LIGHTNING"

    cycle = 60

    attack_power = 15

    chain_count = 3
    chain_range = 200
    damage_rate = 0.8
    first_range = 300

    level_data = [
        {"attack_power": 5},
        {"cycle": -10},
    ]

    def __init__(self):

        cls = type(self)

        super().__init__(
            name=cls.name,
            cycle=cls.cycle,
            attack_power=cls.attack_power,
            level_data=cls.level_data,
        )

        self.chain_count = cls.chain_count
        self.chain_range = cls.chain_range
        self.damage_rate = cls.damage_rate
        self.first_range = cls.first_range

    def update(self, context):

        if self.is_ready():

            self.attack(context)

    def get_lightning_start_position(
        self,
        player,
        hit_enemies,
    ):

        if not hit_enemies:
            return player.x, player.y

        last_enemy = hit_enemies[-1]

        return last_enemy.x, last_enemy.y

    def attack(self, context):

        player = context.player
        enemies = context.enemies

        if not enemies:
            return

        first_targets = get_closest_objects(
            player,
            enemies,
            count=1,
            max_distance=self.first_range,
        )

        if not first_targets:
            return

        current_target = first_targets[0]

        hit_enemies = []

        for _ in range(self.chain_count):

            if current_target is None:
                break

            damage = int(self.attack_power * (self.damage_rate ** len(hit_enemies)))
            
            shield = self.get_shield_at_target(
                context,
                current_target,
            )

            if shield:

                damage_shields_in_circle(
                    context,
                    current_target.x,
                    current_target.y,
                    current_target.hit_radius,
                    damage,
                )

                start_x, start_y = self.get_lightning_start_position(
                    player,
                    hit_enemies,
                )

                add_lightning_effect(
                    context,
                    start_x,
                    start_y,
                    shield.x,
                    shield.y,
                )

                break

            current_target.take_damage(
                context,
                damage,
            )

            start_x, start_y = self.get_lightning_start_position(
                player,
                hit_enemies,
            )

            add_lightning_effect(
                context,
                start_x,
                start_y,
                current_target.x,
                current_target.y,
            )

            hit_enemies.append(current_target)

            next_candidates = [enemy for enemy in enemies if enemy not in hit_enemies]

            next_targets = get_closest_objects(
                current_target,
                next_candidates,
                count=1,
                max_distance=self.chain_range,
            )

            if not next_targets:
                break

            current_target = next_targets[0]
    
    def get_shield_at_target(
        self,
        context,
        target,
    ):

        for enemy in context.enemies:

            if not getattr(enemy, "shield_active", False):
                continue

            distance = math.hypot(
                target.x - enemy.x,
                target.y - enemy.y,
            )

            if distance <= enemy.shield_radius + target.hit_radius:
                return enemy

        return None


class MineWeapon(Weapon):

    weapon_id = "mine_weapon"

    name = "MINE"

    cycle = 120

    attack_power = 30

    explosion_radius = 120

    place_distance = 60

    mine_hit_radius = 50
    mine_draw_radius = 50

    mine_images = []

    level_data = [
        {"attack_power": 10},
        {"cycle": -20},
    ]

    def __init__(self):

        cls = type(self)

        super().__init__(
            name=cls.name,
            cycle=cls.cycle,
            attack_power=cls.attack_power,
            level_data=cls.level_data,
        )

        self.explosion_radius = cls.explosion_radius
        self.place_distance = cls.place_distance
        self.mine_hit_radius = cls.mine_hit_radius
        self.mine_draw_radius = cls.mine_draw_radius

    def update(self, context):

        if self.is_ready():

            self.place_mine(context)

    def place_mine(self, context):

        player = context.player

        x = player.x
        y = player.y

        if player.face == 0:
            y += self.place_distance

        elif player.face == 1:
            y -= self.place_distance

        elif player.face == 2:
            x += self.place_distance

        elif player.face == 3:
            x -= self.place_distance

        mine = Mine(
            x=x,
            y=y,
            attack_power=self.attack_power,
            explosion_radius=self.explosion_radius,
            hit_radius=self.mine_hit_radius,
            draw_radius=self.mine_draw_radius,
            images=self.mine_images,
        )

        context.mines.append(mine)


class HornetNestWeapon(Weapon):

    weapon_id = "hornet_nest_weapon"

    name = "HORNET NEST"

    cycle = 180

    attack_power = 8

    hit_radius = 120
    draw_radius = 25

    duration = 240
    attack_cycle = 30
    poison_rate = 0.3

    nest_images = []
    bee_images = []

    level_data = [
        {"attack_power": 4},
        {"cycle": -30},
        {"hit_radius": 30},
    ]

    def __init__(self):

        cls = type(self)

        super().__init__(
            name=cls.name,
            cycle=cls.cycle,
            attack_power=cls.attack_power,
            level_data=cls.level_data,
        )

        self.hit_radius = cls.hit_radius
        self.draw_radius = cls.draw_radius
        self.duration = cls.duration
        self.attack_cycle = cls.attack_cycle

    def update(self, context):

        if self.is_ready():

            self.place_nest(context)

    def place_nest(self, context):

        x = random.randint(
            int(context.camera_x),
            int(context.camera_x + WIDTH),
        )

        y = random.randint(
            int(context.camera_y),
            int(context.camera_y + HEIGHT),
        )

        nest = HornetNest(
            x=x,
            y=y,
            attack_power=self.attack_power,
            hit_radius=self.hit_radius,
            draw_radius=self.draw_radius,
            duration=self.duration,
            attack_cycle=self.attack_cycle,
            images=self.nest_images,
            bee_images=self.bee_images,
            poison_rate=self.poison_rate,
        )

        context.hornet_nests.append(nest)
