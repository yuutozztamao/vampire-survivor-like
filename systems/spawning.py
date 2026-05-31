import random
from enemy import *

from settings import WIDTH, HEIGHT

enemy_list = [
    {
        "enemy_class": Zombie,
        "spawn_data": {
            "min_time": 0,
            "max_time": 1000,
            "base_spawn_cycle": 80,
            "spawn_cycle": 80,
            "min_spawn_cycle": 40,
            "spawn_timer": 0,
        },
    },
    {
        "enemy_class": MuscleZombie,
        "spawn_data": {
            "min_time": 1000,
            "max_time": 60000,
            "base_spawn_cycle": 50,
            "spawn_cycle": 50,
            "min_spawn_cycle": 30,
            "spawn_timer": 0,
        },
    },
]


def enemy_spawn(enemies, enemy_list, timer, next_enemy_id):

    for enemy_param in enemy_list:

        spawn_data = enemy_param["spawn_data"]
        enemy_class = enemy_param["enemy_class"]

        if spawn_data["min_time"] < timer < spawn_data["max_time"]:

            spawn_data["spawn_cycle"] = max(
                spawn_data["min_spawn_cycle"],
                spawn_data["base_spawn_cycle"] - timer // 1800,
            )

            spawn_data["spawn_timer"] += 1

            if spawn_data["spawn_timer"] > spawn_data["spawn_cycle"]:

                spawn_point_num = random.randint(0, 3)

                # 上
                if spawn_point_num == 0:
                    x = random.randint(0, WIDTH)
                    y = -200

                # 下
                elif spawn_point_num == 1:
                    x = random.randint(0, WIDTH)
                    y = HEIGHT + 200

                # 左
                elif spawn_point_num == 2:
                    x = -200
                    y = random.randint(0, HEIGHT)

                # 右
                else:
                    x = WIDTH + 200
                    y = random.randint(0, HEIGHT)

                new_enemy = enemy_class(
                    next_enemy_id,
                    x,
                    y,
                )

                enemies.append(new_enemy)

                next_enemy_id += 1

                spawn_data["spawn_timer"] = 0

    return next_enemy_id
