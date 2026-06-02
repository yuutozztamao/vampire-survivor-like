import random
from enemy import *

from settings import WIDTH, HEIGHT

enemy_list = [
    {
        "enemy_class": Zombie,
        "spawn_data": {
            "min_time": 3000,
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
            "min_time": 3000,
            "max_time": 60000,
            "base_spawn_cycle": 50,
            "spawn_cycle": 50,
            "min_spawn_cycle": 30,
            "spawn_timer": 0,
        },
    },
    {
        "enemy_class": ShooterZombie,
        "spawn_data": {
            "min_time": 5000,
            "max_time": 60000,
            "base_spawn_cycle": 120,
            "spawn_cycle": 120,
            "min_spawn_cycle": 60,
            "spawn_timer": 0,
        },
    },
    {
        "enemy_class": BoarZombie,
        "spawn_data": {
            "min_time": 500000,
            "max_time": 60000,
            "base_spawn_cycle": 180,
            "spawn_cycle": 180,
            "min_spawn_cycle": 120,
            "spawn_timer": 0,
        },
    },
    {
        "enemy_class": SlimeZombie,
        "spawn_data": {
            "min_time": 500000,
            "max_time": 60000,
            "base_spawn_cycle": 240,
            "spawn_cycle": 240,
            "min_spawn_cycle": 120,
            "spawn_timer": 0,
        },
    },
    {
        "enemy_class": BomberZombie,
        "spawn_data": {
            "min_time": 0,
            "max_time": 60000,
            "base_spawn_cycle": 180,
            "spawn_cycle": 180,
            "min_spawn_cycle": 90,
            "spawn_timer": 0,
        },
    },
]


def enemy_spawn(enemies, context):

    player = context.player
    timer = context.game_timer
    next_enemy_id = context.next_enemy_id

    spawn_margin = 200

    for enemy_param in enemy_list:

        spawn_data = enemy_param["spawn_data"]
        enemy_class = enemy_param["enemy_class"]

        # 時間条件
        if not (spawn_data["min_time"] < timer < spawn_data["max_time"]):
            continue

        # スポーン間隔調整（時間で徐々に難しくなる）
        spawn_data["spawn_cycle"] = max(
            spawn_data["min_spawn_cycle"],
            spawn_data["base_spawn_cycle"] - timer // 1800,
        )

        spawn_data["spawn_timer"] += 1

        if spawn_data["spawn_timer"] <= spawn_data["spawn_cycle"]:
            continue

        # =========================
        # プレイヤー中心のワールドスポーン
        # =========================

        is_boar = enemy_class == BoarZombie

        if is_boar:
            direction = random.randint(2, 3)
        else:
            direction = random.randint(0, 3)

        if direction == 0:
            # 上
            x = random.randint(
                int(player.x - WIDTH / 2),
                int(player.x + WIDTH / 2),
            )
            y = player.y - HEIGHT / 2 - spawn_margin

        elif direction == 1:
            # 下
            x = random.randint(
                int(player.x - WIDTH / 2),
                int(player.x + WIDTH / 2),
            )
            y = player.y + HEIGHT / 2 + spawn_margin

        elif direction == 2:
            # 左
            x = player.x - WIDTH / 2 - spawn_margin
            y = random.randint(
                int(player.y - HEIGHT / 2),
                int(player.y + HEIGHT / 2),
            )

        else:
            # 右
            x = player.x + WIDTH / 2 + spawn_margin
            y = random.randint(
                int(player.y - HEIGHT / 2),
                int(player.y + HEIGHT / 2),
            )

        # =========================
        # スポーン生成
        # =========================

        new_enemy = enemy_class(
            next_enemy_id,
            x,
            y,
        )

        enemies.append(new_enemy)
        next_enemy_id += 1

        spawn_data["spawn_timer"] = 0

    return next_enemy_id
