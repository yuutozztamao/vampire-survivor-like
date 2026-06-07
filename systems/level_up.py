import random
import pygame

from systems.weapon_factory import create_weapon, weapon_registry
from utils import get_weapon_by_id

# =========================
# レベルアップ内容定義
# =========================

level_up_pool = {
    "damage_up": 10,
    "speed_up": 10,
    "pickup_radius": 5,
    "normal_weapon": 3,
    "random_weapon": 3,
    "random_aim_weapon": 2,
    "freeze_weapon": 3,
    "surround_weapon": 2,
    "chain_lightning_weapon": 2,
    "mine_weapon": 2,
    "hornet_nest_weapon": 3,
}

# ステータス強化の内容をまとめた表
# "レベルアップ候補ID": ("強化する変数名", 増やす値)
status_level_up_data = {
    "damage_up": ("attack_rate", 0.2),
    "speed_up": ("speed", 1),
    "pickup_radius": ("pickup_radius", 30),
}


# =========================
# 抽選ロジック（重み付き）
# =========================


def weighted_choice(pool):
    total = sum(pool.values())
    r = random.randint(1, total)

    s = 0
    for k, v in pool.items():
        s += v
        if r <= s:
            return k


# =========================
# 3択生成（重複なし）
# =========================


def get_level_up_choices(pool, count=3):
    choices = []
    temp_pool = pool.copy()

    for _ in range(min(count, len(temp_pool))):
        choice = weighted_choice(temp_pool)
        choices.append(choice)
        temp_pool.pop(choice)

    return choices


# =========================
# ステータス補助関数
# =========================


def add_param(obj, param, value, minimum=None):
    new_value = getattr(obj, param) + value

    if minimum is not None:
        new_value = max(minimum, new_value)

    setattr(obj, param, new_value)


# =========================
# レベルアップ効果（分岐なし設計）
# =========================


def apply_level_up(choice, player, weapons):

    if choice in status_level_up_data:

        param, value = status_level_up_data[choice]

        add_param(player, param, value)

    elif choice in weapon_registry:

        unlock_weapon(weapons, choice)


# =========================
# レベルアッププールを更新（レベルMAXだったらプールから除外）
# =========================


def build_level_up_pool(weapons):

    pool = level_up_pool.copy()

    for key in list(pool):

        weapon = get_weapon_by_id(weapons, key)

        if weapon and weapon.is_max_level:
            pool.pop(key)

    return pool


# =========================
# 武器解放処理（ここに集約）
# =========================


def unlock_weapon(weapons, weapon_id):

    for weapon in weapons:

        if weapon.weapon_id == weapon_id:

            weapon.level_up()
            return

    weapon = create_weapon(weapon_id)

    if weapon is None:
        return

    weapons.append(weapon)


# =========================
# 入力処理（mainから呼ぶだけ）
# =========================


def level_up_select(event, context):

    level_up_choices = context.level_up_choices
    player = context.player
    weapons = context.weapons

    if event.type != pygame.KEYDOWN:
        return None

    key_map = {
        pygame.K_1: 0,
        pygame.K_2: 1,
        pygame.K_3: 2,
    }

    if event.key not in key_map:
        return None

    index = key_map[event.key]

    if index >= len(level_up_choices):
        return None

    choice = level_up_choices[index]

    apply_level_up(choice, player, weapons)

    return choice
