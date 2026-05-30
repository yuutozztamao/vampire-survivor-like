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

    def draw(self, screen):

        screen.blit(self.images[self.image_index], (self.draw_x, self.draw_y))
