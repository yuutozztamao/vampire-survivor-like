import random
from enemy import *

from settings import WIDTH, HEIGHT


def spawn_normal_enemy(enemy_class, context):

    player = context.player
    spawn_margin = 200

    is_boar = enemy_class == BoarZombie

    if is_boar:
        direction = random.randint(2, 3)
    else:
        direction = random.randint(0, 3)

    if direction == 0:
        x = random.randint(
            int(player.x - WIDTH / 2),
            int(player.x + WIDTH / 2),
        )
        y = player.y - HEIGHT / 2 - spawn_margin

    elif direction == 1:
        x = random.randint(
            int(player.x - WIDTH / 2),
            int(player.x + WIDTH / 2),
        )
        y = player.y + HEIGHT / 2 + spawn_margin

    elif direction == 2:
        x = player.x - WIDTH / 2 - spawn_margin
        y = random.randint(
            int(player.y - HEIGHT / 2),
            int(player.y + HEIGHT / 2),
        )

    else:
        x = player.x + WIDTH / 2 + spawn_margin
        y = random.randint(
            int(player.y - HEIGHT / 2),
            int(player.y + HEIGHT / 2),
        )

    new_enemy = enemy_class(
        context.next_enemy_id,
        x,
        y,
    )

    context.enemies.append(new_enemy)
    context.next_enemy_id += 1


def spawn_boar_wall(enemy_class, context):

    player = context.player

    spawn_margin = 250
    gap = 120

    side = random.choice(["left", "right"])

    if side == "left":
        x = player.x - WIDTH / 2 - spawn_margin
        direction = 1
    else:
        x = player.x + WIDTH / 2 + spawn_margin
        direction = -1

    start_y = player.y - HEIGHT / 2
    end_y = player.y + HEIGHT / 2

    y = start_y

    while y <= end_y:

        new_enemy = enemy_class(
            context.next_enemy_id,
            x,
            y,
        )

        new_enemy.direction = direction
        new_enemy.separate = False

        context.enemies.append(new_enemy)
        context.next_enemy_id += 1

        y += gap


enemy_list = [
    {
        "enemy_class": Zombie,
        "spawn_func": spawn_normal_enemy,
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
        "spawn_func": spawn_normal_enemy,
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
        "spawn_func": spawn_normal_enemy,
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
        "spawn_func": spawn_normal_enemy,
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
        "spawn_func": spawn_normal_enemy,
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
        "spawn_func": spawn_normal_enemy,
        "spawn_data": {
            "min_time": 100000,
            "max_time": 60000,
            "base_spawn_cycle": 180,
            "spawn_cycle": 180,
            "min_spawn_cycle": 90,
            "spawn_timer": 0,
        },
    },
    {
        "enemy_class": GhostZombie,
        "spawn_func": spawn_normal_enemy,
        "spawn_data": {
            "min_time": 100000,
            "max_time": 60000,
            "base_spawn_cycle": 180,
            "spawn_cycle": 180,
            "min_spawn_cycle": 90,
            "spawn_timer": 0,
        },
    },
    {
        "enemy_class": BoarZombie,
        "spawn_func": spawn_boar_wall,
        "spawn_data": {
            "min_time": 0,
            "max_time": 60000,
            "base_spawn_cycle": 900,
            "spawn_cycle": 900,
            "min_spawn_cycle": 600,
            "spawn_timer": 0,
        },
    },
]


def enemy_spawn(enemies, context):

    timer = context.game_timer

    for enemy_param in enemy_list:

        spawn_data = enemy_param["spawn_data"]
        enemy_class = enemy_param["enemy_class"]
        spawn_func = enemy_param["spawn_func"]

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

        spawn_func(enemy_class, context)

        spawn_data["spawn_timer"] = 0

    return context.next_enemy_id
