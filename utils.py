import math
import pygame
from settings import WIDTH, HEIGHT


def get_distance_xy(x1, y1, x2, y2):

    dx = x1 - x2
    dy = y1 - y2

    return math.hypot(dx, dy)


def get_direction_and_distance(from_obj, to_obj):

    dx = to_obj.x - from_obj.x
    dy = to_obj.y - from_obj.y

    distance = math.hypot(dx, dy)

    return dx, dy, distance


def is_hit(obj1, obj2):

    distance = get_distance(obj1, obj2)

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

                if enemy1.separate and enemy2.separate:

                    enemy1.x += dx * overlap / 2
                    enemy1.y += dy * overlap / 2

                    enemy2.x -= dx * overlap / 2
                    enemy2.y -= dy * overlap / 2

                elif enemy1.separate and not enemy2.separate:

                    enemy1.x += dx * overlap
                    enemy1.y += dy * overlap

                elif not enemy1.separate and enemy2.separate:

                    enemy2.x -= dx * overlap
                    enemy2.y -= dy * overlap


def enemy_knockback(enemy, source, power=10):

    if getattr(enemy, "shielded", False):
        return

    if not getattr(enemy, "knockback", True):
        return

    dx, dy, distance = get_direction_and_distance(source, enemy)

    if distance == 0:
        return

    enemy.x += dx / distance * power
    enemy.y += dy / distance * power


def get_weapon_by_id(weapons, weapon_id):

    for weapon in weapons:

        if weapon.weapon_id == weapon_id:
            return weapon

    return None


def is_in_camera(
    x,
    y,
    context,
    margin=0,
):

    return (
        context.camera_x - margin <= x <= context.camera_x + WIDTH + margin
        and context.camera_y - margin <= y <= context.camera_y + HEIGHT + margin
    )


def get_distance(obj1, obj2):

    dx = obj1.x - obj2.x
    dy = obj1.y - obj2.y

    return math.hypot(dx, dy)


def get_closest_objects(from_obj, objects, count=1, max_distance=None):

    candidates = []

    for obj in objects:

        distance = get_distance(from_obj, obj)

        if max_distance is not None and distance > max_distance:
            continue

        candidates.append(
            {
                "obj": obj,
                "distance": distance,
            }
        )

    candidates.sort(key=lambda candidate: candidate["distance"])

    return [candidate["obj"] for candidate in candidates[:count]]


def create_white_image(image):

    white_image = image.copy()

    white_image.fill(
        (255, 255, 255),
        special_flags=pygame.BLEND_RGB_MAX,
    )

    return white_image


def is_hit_circle(obj1, x, y, radius):

    distance = get_distance_xy(
        obj1.x,
        obj1.y,
        x,
        y,
    )

    return distance < obj1.hit_radius + radius
