import random
import math

import pygame

from utils import get_distance
from systems.condition import apply_poison
from systems.collision import damage_shields_in_circle

class HornetNest:

    def __init__(
        self,
        x,
        y,
        attack_power,
        hit_radius,
        draw_radius,
        duration,
        attack_cycle,
        images,
        bee_images,
        poison_rate,
    ):

        self.x = x
        self.y = y

        self.attack_power = attack_power

        self.hit_radius = hit_radius
        self.draw_radius = draw_radius

        self.duration = duration
        self.timer = 0

        self.attack_cycle = attack_cycle
        self.attack_timer = 0

        self.poison_rate = poison_rate

        self.dead = False

        self.images = images
        self.image_index = 0

        self.bee_images = bee_images
        self.bee_image_index = 0

        self.bees = []

        for _ in range(20):

            bee = {
                "angle": random.uniform(0, math.pi * 2),
                "distance": random.uniform(30, self.hit_radius),
                "speed": random.uniform(-0.12, 0.12),
                "size": random.randint(4, 7),
            }

            self.bees.append(bee)

    def update(self, context):

        self.timer += 1
        self.attack_timer += 1

        for bee in self.bees:

            bee["angle"] += bee["speed"]

            bee["distance"] += random.uniform(-2, 2)

            bee["distance"] = max(
                15,
                min(
                    self.hit_radius,
                    bee["distance"],
                ),
            )

        if self.attack_timer >= self.attack_cycle:

            self.attack(context)

            self.attack_timer = 0

        if self.timer >= self.duration:

            self.dead = True

    def attack(self, context):

        damage_shields_in_circle(
            context,
            self.x,
            self.y,
            self.hit_radius,
            self.attack_power,
        )

        for enemy in context.enemies[:]:

            distance = get_distance(self, enemy)

            if distance <= self.hit_radius + enemy.hit_radius:

                enemy.take_damage(
                    context,
                    self.attack_power,
                )

                if random.random() < self.poison_rate:

                    apply_poison(enemy)

    def draw(self, screen, context):

        image = self.images[self.image_index]

        cx = context.camera_x
        cy = context.camera_y

        x = self.x - cx
        y = self.y - cy

        screen.blit(
            image,
            (
                self.x - image.get_width() / 2 - cx,
                self.y - image.get_height() / 2 - cy,
            ),
        )

        pygame.draw.circle(
            screen,
            (255, 220, 80),
            (x, y),
            self.hit_radius,
            2,
        )

        for bee in self.bees:

            bee_x = self.x + math.cos(bee["angle"]) * bee["distance"]
            bee_y = self.y + math.sin(bee["angle"]) * bee["distance"]

            bee_image = self.bee_images[self.bee_image_index]

            screen.blit(
                bee_image,
                (
                    bee_x - bee_image.get_width() / 2 - cx,
                    bee_y - bee_image.get_height() / 2 - cy,
                ),
            )
