from utils import is_hit, enemy_knockback


class Bullet:

    def __init__(
        self,
        x,
        y,
        x_speed,
        y_speed,
        hit_radius,
        draw_radius,
        attack_power,
        through,
        images,
        freeze=False,
    ):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.hit_radius = hit_radius
        self.draw_radius = draw_radius
        self.attack_power = attack_power
        self.through = through
        self.hit_enemies = set()
        self.timer = 120
        self.dead = False
        self.image_index = 0
        self.images = images
        self.freeze = freeze

    @property
    def draw_x(self):
        return self.x - self.draw_radius

    @property
    def draw_y(self):
        return self.y - self.draw_radius

    def move(self):

        self.x += self.x_speed
        self.y += self.y_speed

    def hit_check(self, enemies, player, damage_texts, gems):

        for enemy in enemies[:]:

            if is_hit(self, enemy) and enemy.id not in self.hit_enemies:

                enemy.take_damage(
                    player,
                    enemies,
                    self.attack_power,
                    damage_texts,
                    gems,
                )

                enemy_knockback(enemy, self)

                self.hit_enemies.add(enemy.id)

                if not self.through:
                    self.dead = True
                    return

    def check_dead(self):
        self.timer -= 1
        if self.timer <= 0:
            self.dead = True

    def update(self, context):
        self.move()

        self.check_dead()

    def draw(self, screen, context):
        cx = context.camera_x
        cy = context.camera_y

        screen.blit(self.images[self.image_index], (self.draw_x - cx, self.draw_y - cy))
