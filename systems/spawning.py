import random
import math

from enemy import *
from settings import WIDTH, HEIGHT

def get_normal_spawn_position(enemy_class, context):

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

    return x, y


def create_enemy(enemy_class, context, x, y):

    new_enemy = enemy_class(
        context.next_enemy_id,
        x,
        y,
    )

    context.enemies.append(new_enemy)

    context.next_enemy_id += 1

    return new_enemy


def spawn_normal_enemy(enemy_class, context, spawn_data=None):

    x, y = get_normal_spawn_position(
        enemy_class,
        context,
    )

    create_enemy(
        enemy_class,
        context,
        x,
        y,
    )


def spawn_group_enemy(enemy_class, context, spawn_data=None):

    if spawn_data is None:
        spawn_data = {}

    spawn_count = spawn_data.get(
        "spawn_count",
        3,
    )

    group_radius = spawn_data.get(
        "group_radius",
        60,
    )

    base_x, base_y = get_normal_spawn_position(
        enemy_class,
        context,
    )

    for _ in range(spawn_count):

        angle = random.uniform(
            0,
            2 * 3.14159,
        )

        distance = random.uniform(
            0,
            group_radius,
        )

        x = base_x + math.cos(angle) * distance
        y = base_y + math.sin(angle) * distance

        create_enemy(
            enemy_class,
            context,
            x,
            y,
        )


def spawn_boar_wall(enemy_class, context, spawn_data=None):

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

        create_enemy(
            enemy_class,
            context,
            x,
            y,
        )

        y += gap


def spawn_surround_enemy(enemy_class, context, spawn_data=None):

    if spawn_data is None:
        spawn_data = {}

    player = context.player

    spawn_margin = spawn_data.get(
        "spawn_margin",
        200,
    )

    spawn_gap = spawn_data.get(
        "spawn_gap",
        180,
    )

    left_x = player.x - WIDTH / 2 - spawn_margin
    right_x = player.x + WIDTH / 2 + spawn_margin
    top_y = player.y - HEIGHT / 2 - spawn_margin
    bottom_y = player.y + HEIGHT / 2 + spawn_margin

    left = player.x - WIDTH / 2
    right = player.x + WIDTH / 2
    top = player.y - HEIGHT / 2
    bottom = player.y + HEIGHT / 2

    horizontal_count = max(
        1,
        int(WIDTH // spawn_gap) + 1,
    )

    vertical_count = max(
        1,
        int(HEIGHT // spawn_gap) + 1,
    )

    spawn_positions = []

    for i in range(horizontal_count):

        if horizontal_count == 1:
            x = player.x
        else:
            x = left + WIDTH * i / (horizontal_count - 1)

        spawn_positions.append(
            (
                x,
                top_y,
            )
        )

        spawn_positions.append(
            (
                x,
                bottom_y,
            )
        )

    for i in range(vertical_count):

        if vertical_count == 1:
            y = player.y
        else:
            y = top + HEIGHT * i / (vertical_count - 1)

        spawn_positions.append(
            (
                left_x,
                y,
            )
        )

        spawn_positions.append(
            (
                right_x,
                y,
            )
        )

    for x, y in spawn_positions:

        create_enemy(
            enemy_class,
            context,
            x,
            y,
        )


def spawn_boss_enemy(enemy_class, context, spawn_data=None):

    player = context.player

    x = player.x
    y = player.y - HEIGHT / 2 - 200

    new_enemy = create_enemy(
        enemy_class,
        context,
        x,
        y,
    )

    context.boss = new_enemy
    context.boss_area = {
        "left": context.camera_x,
        "top": context.camera_y,
        "right": context.camera_x + WIDTH,
        "bottom": context.camera_y + HEIGHT,
    }


enemy_list = [
    # =========================
    # 3分ボス
    # =========================
    {
        "enemy_class": GuardianZombie,
        "spawn_func": spawn_boss_enemy,
        "spawn_data_list": [
            {
                "min_time": 10,
                "spawned": False,
            },
        ],
    },
    # =========================
    # ボス中だけ出る敵
    # =========================
    {
        "enemy_class": ShieldZombie,
        "spawn_func": spawn_normal_enemy,
        "spawn_data_list": [
            {
                "base_spawn_cycle": 300,
                "min_spawn_cycle": 240,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 10,
                "required_boss_class": GuardianZombie,
            },
        ],
    },
    # =========================
    # 基本敵
    # =========================
    {
        "enemy_class": Zombie,
        "spawn_func": spawn_normal_enemy,
        "spawn_data_list": [
            {
                "min_time": 0,
                "max_time": 60,
                "base_spawn_cycle": 180,
                "min_spawn_cycle": 55,
                "cycle_decrease_interval": 20,
                "cycle_decrease_amount": 5,
                "spawn_func": spawn_surround_enemy,
            },
            {
                "min_time": 60,
                "max_time": 180,
                "base_spawn_cycle": 95,
                "min_spawn_cycle": 60,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 5,
            },
            {
                "min_time": 180,
                "max_time": 60000,
                "base_spawn_cycle": 80,
                "min_spawn_cycle": 45,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 5,
            },
        ],
    },
    # =========================
    # Zombieの群れ
    # =========================
    {
        "enemy_class": Zombie,
        "spawn_func": spawn_group_enemy,
        "spawn_data_list": [
            {
                "min_time": 30,
                "max_time": 120,
                "base_spawn_cycle": 420,
                "min_spawn_cycle": 300,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 20,
                "spawn_count": 4,
                "group_radius": 70,
            },
            {
                "min_time": 180,
                "max_time": 60000,
                "base_spawn_cycle": 360,
                "min_spawn_cycle": 240,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 20,
                "spawn_count": 5,
                "group_radius": 80,
            },
        ],
    },
    # =========================
    # 分裂敵
    # =========================
    {
        "enemy_class": SlimeZombie,
        "spawn_func": spawn_normal_enemy,
        "spawn_data_list": [
            {
                "min_time": 40,
                "max_time": 120,
                "base_spawn_cycle": 240,
                "min_spawn_cycle": 180,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 10,
            },
            {
                "min_time": 180,
                "max_time": 60000,
                "base_spawn_cycle": 300,
                "min_spawn_cycle": 210,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 10,
            },
        ],
    },
    # =========================
    # 中型敵
    # =========================
    {
        "enemy_class": MuscleZombie,
        "spawn_func": spawn_normal_enemy,
        "spawn_data_list": [
            {
                "min_time": 60,
                "max_time": 180,
                "base_spawn_cycle": 100,
                "min_spawn_cycle": 65,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 5,
            },
            {
                "min_time": 180,
                "max_time": 60000,
                "base_spawn_cycle": 110,
                "min_spawn_cycle": 60,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 5,
            },
        ],
    },
    # =========================
    # 遠距離敵
    # =========================
    {
        "enemy_class": ShooterZombie,
        "spawn_func": spawn_normal_enemy,
        "spawn_data_list": [
            {
                "min_time": 90,
                "max_time": 180,
                "base_spawn_cycle": 210,
                "min_spawn_cycle": 140,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 10,
            },
            {
                "min_time": 180,
                "max_time": 60000,
                "base_spawn_cycle": 190,
                "min_spawn_cycle": 110,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 10,
            },
        ],
    },
    # =========================
    # 横移動敵
    # =========================
    {
        "enemy_class": BoarZombie,
        "spawn_func": spawn_normal_enemy,
        "spawn_data_list": [
            {
                "min_time": 120,
                "max_time": 180,
                "base_spawn_cycle": 220,
                "min_spawn_cycle": 160,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 10,
            },
            {
                "min_time": 180,
                "max_time": 60000,
                "base_spawn_cycle": 200,
                "min_spawn_cycle": 130,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 10,
            },
            {
                "min_time": 0,
                "max_time": 60000,
                "base_spawn_cycle": 900,
                "min_spawn_cycle": 600,
                "cycle_decrease_interval": 60,
                "cycle_decrease_amount": 30,
                "spawn_func": spawn_boar_wall,
            },
        ],
    },
    # =========================
    # 四方囲みスポーン
    # =========================
    {
        "enemy_class": Zombie,
        "spawn_func": spawn_surround_enemy,
        "spawn_data_list": [
            {
                "min_time": 150,
                "max_time": 180,
                "base_spawn_cycle": 900,
                "min_spawn_cycle": 700,
                "cycle_decrease_interval": 30,
                "cycle_decrease_amount": 50,
                "spawn_gap": 300,
                "spawn_margin": 220,
            },
            {
                "min_time": 240,
                "max_time": 60000,
                "base_spawn_cycle": 900,
                "min_spawn_cycle": 600,
                "cycle_decrease_interval": 60,
                "cycle_decrease_amount": 50,
                "spawn_gap": 280,
                "spawn_margin": 220,
            },
        ],
    },
    # =========================
    # まだ本格投入しない敵
    # =========================
    {
        "enemy_class": BomberZombie,
        "spawn_func": spawn_normal_enemy,
        "spawn_data_list": [
            {
                "min_time": 100000,
                "max_time": 60000,
                "base_spawn_cycle": 180,
                "min_spawn_cycle": 90,
            },
        ],
    },
    {
        "enemy_class": GhostZombie,
        "spawn_func": spawn_normal_enemy,
        "spawn_data_list": [
            {
                "min_time": 100000,
                "max_time": 60000,
                "base_spawn_cycle": 180,
                "min_spawn_cycle": 90,
            },
        ],
    },
]


def enemy_spawn(context):

    timer = context.spawn_timer_sec

    for enemy_param in enemy_list:

        enemy_class = enemy_param["enemy_class"]
        default_spawn_func = enemy_param["spawn_func"]

        spawn_data_list = enemy_param["spawn_data_list"]

        for spawn_data in spawn_data_list:

            spawn_func = spawn_data.get(
                "spawn_func",
                default_spawn_func,
            )

            if spawn_data.get("spawned", False):
                continue

            required_boss_class = spawn_data.get("required_boss_class")

            if required_boss_class is not None:

                if not context.boss_active:
                    continue

                if not isinstance(context.boss, required_boss_class):
                    continue

            elif context.boss_active:

                continue

            # 時間条件
            min_time = spawn_data.get("min_time")
            max_time = spawn_data.get("max_time")

            if min_time is not None and timer <= min_time:
                continue

            if max_time is not None and timer >= max_time:
                continue

            # 1回だけ出現する敵
            if "spawned" in spawn_data:

                spawn_func(enemy_class, context, spawn_data)

                spawn_data["spawned"] = True

                continue

            # スポーン間隔調整（時間で徐々に難しくなる）
            base_spawn_cycle = spawn_data["base_spawn_cycle"]

            min_spawn_cycle = spawn_data.get(
                "min_spawn_cycle",
                base_spawn_cycle,
            )

            cycle_decrease_interval = spawn_data.get(
                "cycle_decrease_interval",
                30,
            )

            cycle_decrease_amount = spawn_data.get(
                "cycle_decrease_amount",
                5,
            )

            min_time = spawn_data.get(
                "min_time",
                0,
            )

            elapsed_time = max(
                timer - min_time,
                0,
            )

            decrease_count = elapsed_time // cycle_decrease_interval

            spawn_data["spawn_cycle"] = max(
                min_spawn_cycle,
                base_spawn_cycle - decrease_count * cycle_decrease_amount,
            )

            spawn_data["spawn_timer"] = spawn_data.get("spawn_timer", 0) + 1

            if spawn_data["spawn_timer"] <= spawn_data["spawn_cycle"]:
                continue

            spawn_func(enemy_class, context, spawn_data)

            spawn_data["spawn_timer"] = 0

    return context.next_enemy_id
