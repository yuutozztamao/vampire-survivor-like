import pygame
import random
import math

from settings import WIDTH
from systems.ui import draw_entity_health_bar, draw_bar
from systems.effect import add_explosion_effect
from utils import (
    is_in_camera,
    get_direction_and_distance,
    get_distance,
    create_white_image,
    get_closest_objects,
)
from gem import Gem
from enemy_bullet import EnemyBullet

class Enemy:

    health_bar_height = 7
    health_bar_back_color = (100, 100, 100)
    health_bar_color = (255, 0, 0)

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
        self.separate = True
        self.health_bar_timer = 0
        self.hit_effect_timer = 0
        self.image_index = 0

        self.frozen_timer = 0
        self.frozen_rate = 0.5
        self.freeze_effect_timer = 0
        self.freeze_particles = []

        self.poison_timer = 0
        self.poison_damage_timer = 0
        self.poison_bubble_timer = 0
        self.poison_bubbles = []

        self.shield_count = 0

    @property
    def draw_x(self):
        return self.x - self.draw_radius

    @property
    def draw_y(self):
        return self.y - self.draw_radius

    @property
    def is_blinking(self):

        return self.hit_effect_timer % 2 > 0

    @property
    def current_image(self):

        return self.images[self.image_index]

    @property
    def draw_image(self):

        if self.is_blinking:
            return create_white_image(self.current_image)

        return self.current_image

    @property
    def health_bar_length(self):

        return self.hit_radius + 10

    @property
    def health_bar_y(self):

        return self.y + self.draw_radius

    @property
    def health_bar_value(self):

        return self.health

    @property
    def health_bar_max_value(self):

        return self.max_health

    @property
    def health_bar_visible(self):

        return self.health_bar_timer > 0

    @property
    def shielded(self):

        return self.shield_count > 0
    # =========================
    # 更新処理
    # =========================

    def update(self, context):

        self.move(context.player)

        self.update_status_effects(context)

        self.update_visual_effects()

        self.update_ui_timers()

    def move(self, player):

        current_speed = self.get_current_speed()

        dx, dy, distance = get_direction_and_distance(self, player)

        if distance != 0:
            self.x += dx / distance * current_speed
            self.y += dy / distance * current_speed

    def get_current_speed(self):

        if self.frozen_timer > 0:
            return self.speed * self.frozen_rate

        return self.speed

    def update_status_effects(self, context):

        self.update_frozen()

        self.update_poison(context)

    def update_frozen(self):

        if self.frozen_timer <= 0:
            return

        self.frozen_timer -= 1

        self.freeze_effect_timer += 1

    def update_poison(self, context):

        if self.poison_timer <= 0:
            return

        self.poison_timer -= 1

        self.poison_damage_timer += 1

        if self.poison_damage_timer >= 30:

            self.take_damage(
                context,
                1,
            )

            self.poison_damage_timer = 0

    def update_visual_effects(self):

        self.update_poison_visual()

        self.update_poison_bubbles()

        self.update_freeze_effect()

    def update_poison_visual(self):

        if self.poison_timer <= 0:
            return

        self.poison_bubble_timer += 1

        if self.poison_bubble_timer >= 10:

            self.create_poison_bubble()

            self.poison_bubble_timer = 0

    def create_poison_bubble(self):

        bubble = {
            "x_offset": random.uniform(
                -self.draw_radius * 0.6,
                self.draw_radius * 0.6,
            ),
            "y_offset": self.draw_radius * 0.6,
            "speed": random.uniform(0.5, 1.5),
            "size": random.randint(3, 6),
            "timer": 40,
        }

        self.poison_bubbles.append(bubble)

    def update_poison_bubbles(self):

        for bubble in self.poison_bubbles[:]:

            bubble["y_offset"] -= bubble["speed"]

            bubble["timer"] -= 1

            if bubble["timer"] <= 0:
                self.poison_bubbles.remove(bubble)

    def update_freeze_effect(self):

        if self.freeze_effect_timer >= 10:

            particle = {
                "x_offset": random.uniform(
                    -self.draw_radius * 0.8,
                    self.draw_radius * 0.8,
                ),
                "y_offset": -self.draw_radius,
                "speed": random.uniform(0.5, 1.5),
                "timer": 40,
            }

            self.freeze_particles.append(particle)

            self.freeze_effect_timer = 0

        for particle in self.freeze_particles[:]:

            particle["y_offset"] += particle["speed"]

            particle["timer"] -= 1

            if particle["timer"] <= 0:

                self.freeze_particles.remove(particle)

    def update_ui_timers(self):

        self.hit_effect_timer = max(
            self.hit_effect_timer - 1,
            0,
        )

        self.health_bar_timer = max(
            self.health_bar_timer - 1,
            0,
        )

    # =========================
    # 描画処理
    # =========================

    def draw(self, screen, context):

        self.draw_sprite(screen, context)

        self.draw_health_bar(screen, context)

        self.draw_poison_bubbles(screen, context)

        self.draw_freeze_particles(screen, context)

    def draw_sprite(self, screen, context):

        cx = context.camera_x
        cy = context.camera_y

        screen.blit(
            self.draw_image,
            (self.draw_x - cx, self.draw_y - cy),
        )

    def draw_health_bar(self, screen, context):

        draw_entity_health_bar(
            screen,
            context,
            self,
        )

    def draw_poison_bubbles(self, screen, context):

        cx = context.camera_x
        cy = context.camera_y

        for bubble in self.poison_bubbles:

            bubble_x = self.x + bubble["x_offset"]
            bubble_y = self.y + bubble["y_offset"]

            image = self.poison_bubble_images[0]

            screen.blit(
                image,
                (
                    bubble_x - image.get_width() / 2 - cx,
                    bubble_y - image.get_height() / 2 - cy,
                ),
            )

    def draw_freeze_particles(self, screen, context):

        cx = context.camera_x
        cy = context.camera_y

        for particle in self.freeze_particles:

            snow_x = self.x + particle["x_offset"]
            snow_y = self.y + particle["y_offset"]

            image = self.freeze_particle_images[0]

            screen.blit(
                image,
                (
                    snow_x - image.get_width() / 2 - cx,
                    snow_y - image.get_height() / 2 - cy,
                ),
            )

    # =========================
    # ダメージ処理
    # =========================

    def take_damage(self, context, base_attack_power):
        
        if self.shielded:
            return
        
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

        if self.health <= 0:

            self.die(context)

    def die(self, context):

        self.drop_gem(context)

        self.spawn_children(context)

        self.remove_self(context)

    def drop_gem(self, context):

        new_gem = Gem(
            self.x,
            self.y,
            self.exp,
        )

        context.gems.append(new_gem)

    def spawn_children(self, context):

        pass

    def remove_self(self, context):

        context.enemies.remove(self)


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

        current_speed = self.get_current_speed()

        dx, dy, distance = get_direction_and_distance(self, player)

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
        self.separate = False

    def move(self, player):

        current_speed = self.get_current_speed()

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
    
    def spawn_children(self, context):

        if self.split_count <= 0:
            return

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

        distance = get_distance(self, player)

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

            add_explosion_effect(
                context,
                self.x,
                self.y,
                self.explosion_radius,
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


class GhostZombie(Enemy):

    images = []

    hit_radius = 35
    draw_radius = 35

    speed = 1.1

    max_health = 25

    attack_power = 15

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

        self.ghost = True
        self.alpha = 100
        self.materializing = False
        self.materialize_distance = 170

    def update(self, context):

        super().update(context)

        if not self.ghost and not self.materializing:
            return

        player = context.player

        distance = get_distance(
            self,
            player,
        )

        if distance < self.materialize_distance:
            self.materializing = True
            self.ghost = False

        if self.materializing:

            self.alpha += 3

            if self.alpha >= 255:

                self.alpha = 255
                self.materializing = False
                self.ghost = False

    def draw(self, screen, context):

        if not self.materializing and not self.ghost:
            super().draw(screen, context)
            return

        image = self.images[self.image_index].copy()

        image.set_alpha(self.alpha)

        cx = context.camera_x
        cy = context.camera_y

        screen.blit(
            image,
            (
                self.draw_x - cx,
                self.draw_y - cy,
            ),
        )

        self.draw_health_bar(screen, context)


class ShieldZombie(Enemy):

    images = []

    hit_radius = 45
    draw_radius = 45

    speed = 1.5

    max_health = 60

    attack_power = 10

    shield_radius = 170
    shield_max_health = 40
    shield_color = (80, 180, 255)
    shield_hit_color = (255, 255, 255)
    shield_bar_back_color = (60, 60, 60)
    shield_bar_height = 8
    shield_bar_offset_y = 12
    shield_break_effect_color = (80, 180, 255, 100)

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
        self.shield_health = self.shield_max_health

        self.shield_regen_timer = 0
        self.shield_regen_cycle = 240
        self.shield_hit_timer = 0

    @property
    def shield_active(self):

        return self.shield_health > 0

    @property
    def shield_bar_length(self):

        return self.health_bar_length

    @property
    def shield_bar_y(self):

        return self.y + self.draw_radius + self.shield_bar_offset_y

    def update(self, context):

        target = self.get_target_enemy(context)

        if target:

            current_speed = self.get_current_speed()

            dx, dy, distance = get_direction_and_distance(
                self,
                target,
            )

            if distance > 100 and distance != 0:

                self.x += dx / distance * current_speed
                self.y += dy / distance * current_speed

        self.keep_distance_from_other_shields(context)

        self.update_status_effects(context)

        self.update_visual_effects()

        self.update_ui_timers()

        self.update_shield_regen()

        self.update_shield_hit_effect()

        if self.shield_active:

            self.update_shield_targets(context)

    def update_shield_regen(self):

        if self.shield_active:
            return

        self.shield_regen_timer += 1

        if self.shield_regen_timer >= self.shield_regen_cycle:

            self.shield_health = self.shield_max_health

            self.shield_regen_timer = 0

    def update_shield_hit_effect(self):

        self.shield_hit_timer = max(
            self.shield_hit_timer - 1,
            0,
        )

    def get_target_enemy(self, context):

        targets = get_closest_objects(
            context.player,
            [
                enemy
                for enemy in context.enemies
                if enemy is not self
            ],
            count=1,
        )

        if not targets:
            return None

        return targets[0]

    def keep_distance_from_other_shields(self, context):

        current_speed = self.get_current_speed()

        for enemy in context.enemies:

            if enemy is self:
                continue

            if not isinstance(enemy, ShieldZombie):
                continue

            dx, dy, distance = get_direction_and_distance(
                self,
                enemy,
            )

            min_distance = self.shield_radius + enemy.shield_radius

            if distance >= min_distance:
                continue

            if distance == 0:
                dx = random.uniform(-1, 1)
                dy = random.uniform(-1, 1)
                distance = math.hypot(
                    dx,
                    dy,
                )

            self.x -= dx / distance * current_speed
            self.y -= dy / distance * current_speed

    def move(self, player):

        pass

    def get_shield_targets(self, context):

        if not self.shield_active:
            return []

        targets = []

        for enemy in context.enemies:

            distance = get_distance(
                self,
                enemy,
            )

            if distance <= self.shield_radius:

                targets.append(enemy)

        return targets

    def update_shield_targets(self, context):

        shield_targets = self.get_shield_targets(context)

        for enemy in shield_targets:

            enemy.shield_count += 1

    def draw(self, screen, context):

        super().draw(screen, context)

        if not self.shield_active:

            self.draw_shield_regen_bar(
                screen,
                context,
            )

            return

        cx = context.camera_x
        cy = context.camera_y

        shield_color = self.shield_color

        if self.shield_hit_timer > 0:

            shield_color = self.shield_hit_color

        pygame.draw.circle(
            screen,
            shield_color,
            (
                self.x - cx,
                self.y - cy,
            ),
            self.shield_radius,
            2,
        )

        self.draw_shield_bar(
            screen,
            context,
        )

    def draw_shield_value_bar(
        self,
        screen,
        context,
        value,
        max_value,
    ):

        cx = context.camera_x
        cy = context.camera_y

        length = self.shield_bar_length

        x = self.x - length / 2 - cx
        y = self.shield_bar_y - cy

        draw_bar(
            screen,
            length,
            value,
            max_value,
            self.shield_bar_height,
            x,
            y,
            self.shield_bar_back_color,
            self.shield_color,
        )

    def draw_shield_bar(
        self,
        screen,
        context,
    ):

        if not self.shield_active:
            return

        self.draw_shield_value_bar(
            screen,
            context,
            self.shield_health,
            self.shield_max_health,
        )

    def draw_shield_regen_bar(
        self,
        screen,
        context,
    ):

        self.draw_shield_value_bar(
            screen,
            context,
            self.shield_regen_timer,
            self.shield_regen_cycle,
        )

    def take_shield_damage(
        self,
        context,
        damage,
    ):

        if not self.shield_active:
            return

        self.shield_health -= damage
        self.shield_hit_timer = 5

        if self.shield_health <= 0:

            self.shield_health = 0

            add_explosion_effect(
                context,
                self.x,
                self.y,
                self.shield_radius,
                timer=15,
                color=self.shield_break_effect_color,
            )


class GuardianZombie(Enemy):

    images = []
    bullet_images = []

    hit_radius = 90
    draw_radius = 90

    bullet_hit_radius = 25
    bullet_draw_radius = 25
    bullet_speed = 4
    bullet_attack_power = 15

    speed = 0.7

    max_health = 300

    attack_power = 30

    exp = 300

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
        self.charge_timer = 0
        self.charge_cycle = 300
        self.charging = False
        self.charge_duration = 45
        self.charge_duration_timer = 0
        self.charge_preparing = False
        self.charge_prepare_timer = 0
        self.charge_prepare_cycle = 60

        self.charge_speed = 6
        self.charge_dx = 0
        self.charge_dy = 0

        self.shoot_timer = 0
        self.shoot_cycle = 90

        self.separate = False
        self.knockback = False

    @property
    def health_bar_visible(self):

        return True

    def is_inside_boss_area(self, context):

        if not context.boss_area:
            return True

        area = context.boss_area

        return (
            area["left"] + self.hit_radius <= self.x <= area["right"] - self.hit_radius
            and area["top"] + self.hit_radius <= self.y <= area["bottom"] - self.hit_radius
        )

    def update(self, context):

        if not self.is_inside_boss_area(context):

            super().update(context)

            return

        if self.charge_preparing:

            self.update_charge_prepare(context)

        elif self.charging:

            self.update_charge(context)

        else:

            super().update(context)

            self.update_shoot(context)

            self.start_charge_if_ready(context)

    def draw(self, screen, context):

        image = self.images[self.image_index]

        red_power = 0

        if self.charge_preparing:

            ratio = self.charge_prepare_timer / self.charge_prepare_cycle

            red_power = int(140 * ratio)

        elif self.charging:

            red_power = 140

        draw_image = image.copy()

        if red_power > 0:

            draw_image.fill(
                (
                    red_power,
                    0,
                    0,
                ),
                special_flags=pygame.BLEND_RGB_ADD,
            )

        cx = context.camera_x
        cy = context.camera_y

        screen.blit(
            draw_image,
            (
                self.draw_x - cx,
                self.draw_y - cy,
            ),
        )

        self.draw_health_bar(
            screen,
            context,
        )

        self.draw_poison_bubbles(
            screen,
            context,
        )

        self.draw_freeze_particles(
            screen,
            context,
        )

    def start_charge_if_ready(self, context):

        self.charge_timer += 1

        if self.charge_timer < self.charge_cycle:
            return

        player = context.player

        dx, dy, distance = get_direction_and_distance(
            self,
            player,
        )

        if distance == 0:
            return

        self.charge_dx = dx / distance
        self.charge_dy = dy / distance

        self.charge_preparing = True
        self.charge_prepare_timer = 0
        self.charge_timer = 0

    def update_charge_prepare(self, context):

        self.charge_prepare_timer += 1

        self.update_status_effects(context)

        self.update_visual_effects()

        self.update_ui_timers()

        if self.charge_prepare_timer >= self.charge_prepare_cycle:

            self.charge_preparing = False
            self.charging = True

    def update_charge(self, context):

        next_x = self.x + self.charge_dx * self.charge_speed
        next_y = self.y + self.charge_dy * self.charge_speed

        if context.boss_area:

            area = context.boss_area

            left_limit = area["left"] + self.hit_radius
            right_limit = area["right"] - self.hit_radius
            top_limit = area["top"] + self.hit_radius
            bottom_limit = area["bottom"] - self.hit_radius

            hit_wall = False

            if next_x < left_limit:

                next_x = left_limit
                hit_wall = True

            elif next_x > right_limit:

                next_x = right_limit
                hit_wall = True

            if next_y < top_limit:

                next_y = top_limit
                hit_wall = True

            elif next_y > bottom_limit:

                next_y = bottom_limit
                hit_wall = True

            self.x = next_x
            self.y = next_y

            if hit_wall:

                self.charging = False

        else:

            self.x = next_x
            self.y = next_y

        self.update_status_effects(context)

        self.update_visual_effects()

        self.update_ui_timers()

    def update_shoot(self, context):

        self.shoot_timer += 1

        if self.shoot_timer < self.shoot_cycle:
            return

        player = context.player

        base_angle = math.atan2(
            player.y - self.y,
            player.x - self.x,
        )

        angle_offsets = [
            -30,
            0,
            30,
        ]

        for offset in angle_offsets:

            angle = base_angle + math.radians(offset)

            target_x = self.x + math.cos(angle) * 100
            target_y = self.y + math.sin(angle) * 100

            new_bullet = EnemyBullet(
                x=self.x,
                y=self.y,
                target_x=target_x,
                target_y=target_y,
                attack_power=self.bullet_attack_power,
                images=self.bullet_images,
                hit_radius=self.bullet_hit_radius,
                draw_radius=self.bullet_draw_radius,
                speed=self.bullet_speed,
            )

            context.enemy_bullets.append(new_bullet)

        self.shoot_timer = 0
