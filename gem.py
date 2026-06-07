from utils import get_direction_and_distance


class Gem:

    draw_radius = 15
    hit_radius = 15
    images = []

    def __init__(self, x, y, exp):
        self.x = x
        self.y = y
        self.exp = exp
        self.image_index = 0

    @property
    def draw_x(self):
        return self.x - self.draw_radius

    @property
    def draw_y(self):
        return self.y - self.draw_radius

    def update(self, context):

        player = context.player

        dx, dy, distance = get_direction_and_distance(self, player)

        if distance < player.pickup_radius and distance > 0:

            speed = max(8, distance / 10)

            self.x += dx / distance * speed
            self.y += dy / distance * speed

    def draw(self, screen, context):
        cx = context.camera_x
        cy = context.camera_y

        screen.blit(self.images[self.image_index], (self.draw_x - cx, self.draw_y - cy))
