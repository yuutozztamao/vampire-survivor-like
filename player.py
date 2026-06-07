import pygame

from settings import WIDTH, HEIGHT
from utils import create_white_image
from systems.ui import draw_entity_health_bar

class Player:

    draw_radius = 35
    images = []

    health_bar_height = 7
    health_bar_back_color = (100, 100, 100)
    health_bar_color = (0, 255, 0)
    health_bar_visible = True

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
        self.image_index = 0

    @property
    def draw_x(self):
        return self.x - self.draw_radius

    @property
    def draw_y(self):
        return self.y - self.draw_radius

    @property
    def is_blinking(self):

        return (
            self.invincible_timer > 0
            and self.invincible_timer % 6 > 4
        )

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
        return self.draw_radius + 20

    @property
    def health_bar_y(self):

        return self.y + self.hit_radius

    @property
    def health_bar_value(self):

        return self.health

    @property
    def health_bar_max_value(self):

        return self.max_health

    def update(self, context):

        self.move(context)

        self.update_timers()

    def update_timers(self):

        self.invincible_timer = max(
            self.invincible_timer - 1,
            0,
        )

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

        self.draw_sprite(screen, context)

        self.draw_health_bar(screen, context)

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
