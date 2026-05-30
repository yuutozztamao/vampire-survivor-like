import pygame
from settings import WIDTH, HEIGHT


def draw_exp_bar(screen, player, need_exp):

    length = WIDTH
    value = player.exp
    max_value = need_exp
    height = 15
    x = 0
    y = HEIGHT - height
    back_color = (100, 100, 100)
    bar_color = (0, 0, 100)

    draw_bar(screen, length, value, max_value, height, x, y, back_color, bar_color)


def draw_level_up(screen, font, level_up_choices):

    title = font.render(
        "LEVEL UP!",
        True,
        (255, 255, 255),
    )

    screen.blit(title, (250, 150))

    for i, choice in enumerate(level_up_choices):

        text = font.render(
            f"{i + 1} : {get_display_name(choice)}",
            True,
            (255, 255, 255),
        )

        screen.blit(text, (250, 250 + i * 50))


def get_display_name(choice):

    name_map = {
        "damage_up": "Attack Up",
        "speed_up": "Speed Up",
        "normal_weapon": "Normal Weapon",
        "random_weapon": "Random Weapon",
        "random_aim_weapon": "Aim Weapon",
        "freeze_weapon": "Freeze Weapon",
        "surround_weapon": "Surround Weapon",
    }

    return name_map.get(choice, choice)


# ダメージ文字描画
def draw_damage_texts(screen, damage_texts, font):

    for text in damage_texts:

        damage_surface = font.render(
            str(text["damage"]),
            True,
            (255, 255, 255),
        )

        screen.blit(
            damage_surface,
            (text["x"], text["y"]),
        )


# 経過時間描画
def draw_timer(screen, font, game_timer):

    # フレーム → 秒
    total_seconds = game_timer // 60

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    # 00:00形式
    time_text = f"{minutes:02}:{seconds:02}"

    text = font.render(
        time_text,
        True,
        (255, 255, 255),
    )

    screen.blit(text, (20, 20))


def draw_bar(screen, length, value, max_value, height, x, y, back_color, bar_color):
    if max_value <= 0:
        return

    # 背景
    pygame.draw.rect(
        screen,
        back_color,
        (x, y, length, height),
    )
    # バー本体
    pygame.draw.rect(screen, bar_color, (x, y, (length * value / max_value), height))
