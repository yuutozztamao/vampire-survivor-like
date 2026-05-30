import math
import pygame


def is_hit(obj1, obj2):

    dx = obj1.x - obj2.x
    dy = obj1.y - obj2.y

    distance = math.hypot(dx, dy)

    return distance < obj1.hit_radius + obj2.hit_radius


def enemy_separate(enemies):

    for i in range(len(enemies)):

        enemy1 = enemies[i]

        for j in range(i + 1, len(enemies)):

            enemy2 = enemies[j]

            dx = enemy1.x - enemy2.x
            dy = enemy1.y - enemy2.y

            distance = math.hypot(dx, dy)

            min_distance = enemy1.draw_radius + enemy2.draw_radius

            if distance < min_distance and distance != 0:

                overlap = min_distance - distance

                dx /= distance
                dy /= distance

                enemy1.x += dx * overlap / 2
                enemy1.y += dy * overlap / 2

                enemy2.x -= dx * overlap / 2
                enemy2.y -= dy * overlap / 2


def enemy_knockback(enemy, bullet):
    # ノックバック
    enemy.x += bullet.x_speed * 2
    enemy.y += bullet.y_speed * 2
