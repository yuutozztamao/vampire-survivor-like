import math

class EnemyBullet:

    def __init__(
        self,
        x,
        y,
        target_x,
        target_y,
        attack_power,
        images,
        hit_radius,
        draw_radius,
        speed,
    ):
        self.speed = speed
        self.x = x
        self.y = y
        dx = target_x - x
        dy = target_y - y

        distance = math.hypot(dx, dy)

        if distance == 0:
            distance = 1

        self.x_speed = dx / distance * self.speed
        self.y_speed = dy / distance * self.speed

        self.dead = False

        self.attack_power = attack_power

        self.images = images
        self.image_index = 0
        self.hit_radius = hit_radius
        self.draw_radius = draw_radius

    def update(self, context):

        self.x += self.x_speed
        self.y += self.y_speed

        if (
            abs(self.x - context.player.x) > 2000
            or abs(self.y - context.player.y) > 2000
        ):
            self.dead = True

    def draw(self, screen, context):

        cx = context.camera_x
        cy = context.camera_y

        screen.blit(
            self.images[self.image_index],
            (
                self.x - self.draw_radius - cx,
                self.y - self.draw_radius - cy,
            ),
        )
