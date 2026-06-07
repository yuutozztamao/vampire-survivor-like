import pygame
from utils import get_distance
from systems.collision import damage_shields_in_circle
from systems.effect import add_explosion_effect

class Mine:

    def __init__(
        self,
        x,
        y,
        attack_power,
        explosion_radius,
        hit_radius,
        draw_radius,
        images,
    ):

        self.x = x
        self.y = y

        self.hit_radius = hit_radius
        self.draw_radius = draw_radius

        self.attack_power = attack_power
        self.explosion_radius = explosion_radius

        self.images = images
        self.image_index = 0

        self.explode_timer = 0
        self.explode_cycle = 30
        self.exploding = False

        self.dead = False

    @property
    def draw_x(self):

        return self.x - self.draw_radius

    @property
    def draw_y(self):

        return self.y - self.draw_radius

    def update(self, context):

        if self.exploding:

            self.explode_timer += 1

            if self.explode_timer >= self.explode_cycle:
                
                damage_shields_in_circle(
                    context,
                    self.x,
                    self.y,
                    self.explosion_radius,
                    self.attack_power,
                )
                
                for enemy in context.enemies[:]:

                    distance = get_distance(self, enemy)

                    if distance <= self.explosion_radius + enemy.hit_radius:

                        enemy.take_damage(
                            context,
                            self.attack_power,
                        )

                add_explosion_effect(
                    context,
                    self.x,
                    self.y,
                    self.explosion_radius,
                )

                self.dead = True

    def draw(self, screen, context):

        image = self.images[self.image_index]

        if self.exploding:
            ratio = self.explode_timer / self.explode_cycle
            scale = 1 + ratio * 0.5

            width = int(image.get_width() * scale)
            height = int(image.get_height() * scale)

            image = pygame.transform.scale(
                image,
                (width, height),
            )

        cx = context.camera_x
        cy = context.camera_y

        screen.blit(
            image,
            (
                self.x - image.get_width() / 2 - cx,
                self.y - image.get_height() / 2 - cy,
            ),
        )
