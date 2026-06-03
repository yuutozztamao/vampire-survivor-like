import pygame


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
        self.explode_cycle = 100
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

            self.draw_radius += 1

            self.explode_timer += 1

            if self.explode_timer >= self.explode_cycle:

                context.explosions.append(
                    {
                        "x": self.x,
                        "y": self.y,
                        "radius": self.explosion_radius,
                        "timer": 20,
                    }
                )

                self.dead = True

    def draw(self, screen, context):

        image = self.images[self.image_index]
        cx = context.camera_x
        cy = context.camera_y

        screen.blit(
            image,
            (
                self.draw_x - cx,
                self.draw_y - cy,
            ),
        )
