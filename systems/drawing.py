import pygame
import random

from settings import WIDTH, HEIGHT, CARD_WIDTH_RATIO, CARD_HEIGHT_RATIO
from utils import get_weapon_by_id
from systems.weapon_factory import weapon_registry
from systems.ui import draw_bar


def draw_exp_bar(screen, context):

    player = context.player
    need_exp = context.need_exp

    length = WIDTH
    value = player.exp
    max_value = need_exp
    height = 15
    x = 0
    y = HEIGHT - height
    back_color = (100, 100, 100)
    bar_color = (0, 0, 100)

    draw_bar(screen, length, value, max_value, height, x, y, back_color, bar_color)


def draw_level_up(screen, font, context):

    level_up_choices = context.level_up_choices
    weapons = context.weapons

    title = font.render(
        "LEVEL UP!",
        True,
        (255, 255, 255),
    )

    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 6))

    screen.blit(title, title_rect)

    card_width = WIDTH * CARD_WIDTH_RATIO
    card_height = HEIGHT * CARD_HEIGHT_RATIO

    gap = WIDTH // 40

    total_width = card_width * len(level_up_choices) + gap * (len(level_up_choices) - 1)

    start_x = (screen.get_width() - total_width) // 2

    card_y = 170

    small_font = pygame.font.SysFont(
        None,
        30,
    )

    for i, choice in enumerate(level_up_choices):

        card_x = start_x + i * (card_width + gap)

        card_rect = pygame.Rect(
            card_x,
            card_y,
            card_width,
            card_height,
        )

        # カード背景
        pygame.draw.rect(
            screen,
            (60, 60, 60),
            card_rect,
            border_radius=10,
        )

        # カード枠
        pygame.draw.rect(
            screen,
            (220, 220, 220),
            card_rect,
            width=3,
            border_radius=10,
        )

        # 選択キー
        key_text = font.render(
            f"[{i + 1}]",
            True,
            (255, 255, 100),
        )

        screen.blit(
            key_text,
            (card_x + 80, card_y + 15),
        )

        # タイトル
        title_lines = wrap_text(
            get_display_name(choice, weapons),
            font,
            card_width - 20,
        )

        for line_index, line in enumerate(title_lines):

            title_text = font.render(
                line,
                True,
                (255, 255, 255),
            )

            title_rect = title_text.get_rect(
                center=(
                    card_x + card_width // 2,
                    card_y + 80 + line_index * 35,
                )
            )

            screen.blit(
                title_text,
                title_rect,
            )

        # 説明取得
        description = get_level_up_description(
            choice,
            weapons,
        )

        description = description.replace(
            ", ",
            "\n",
        )

        # 説明文
        description_lines = []

        for line in description.split("\n"):

            description_lines.extend(
                wrap_text(
                    line,
                    small_font,
                    card_width - 20,
                )
            )

        for line_index, line in enumerate(description_lines):

            desc_text = small_font.render(
                line,
                True,
                (180, 180, 180),
            )

            screen.blit(
                desc_text,
                (
                    card_x + 15,
                    card_y + 150 + line_index * 28,
                ),
            )


def get_display_name(choice, weapons):

    weapon = get_weapon_by_id(
        weapons,
        choice,
    )

    # 所持済み武器
    if weapon:

        return f"{weapon.name} +Level"

    # 未所持武器
    weapon_class = weapon_registry.get(choice)

    if weapon_class:

        return f"{weapon_class.name} UNLOCK"

    # レベルアップ候補のIDを、カードUIのタイトルとして画面に表示する名前に変換する表
    # 例: "damage_up" → "Attack"
    name_map = {
        "damage_up": "Attack",
        "speed_up": "Speed",
        "pickup_radius": "Pickup Range",
    }

    return name_map.get(choice, choice)


def get_level_up_description(choice, weapons):

    weapon = get_weapon_by_id(
        weapons,
        choice,
    )

    if weapon:

        # 武器の強化内容の変数名を、カードUIの説明文として画面に表示する名前に変換する表
        # 例: "attack_power" → "Attack"
        effect_map = {
            "cycle": "Cycle",
            "attack_power": "Attack",
            "bullet_speed": "Bullet Speed",
            "shot_count": "Shot Count",
            "outer_hit_radius": "Area Size",
            "inner_hit_radius": "Inner Radius",
            "chain_count": "Chain Count",
            "chain_range": "Chain Range",
            "first_range": "First Range",
            "explosion_radius": "Explosion Radius",
            "place_distance": "Place Distance",
            "poison_rate": "Poison Rate",
        }

        texts = []

        for param, value in weapon.next_level_data.items():

            name = effect_map.get(
                param,
                param,
            )

            if isinstance(value, float):
                value = f"{value * 100:.0f}%" if "rate" in param else value

            sign = "+" if value > 0 else ""

            texts.append(f"{name} {sign}{value}")

        return ", ".join(texts)

    description_map = {
        "damage_up": "Attack +20%",
        "speed_up": "Speed +1",
        "pickup_radius": "Pickup Range +50",
    }

    return description_map.get(choice, "")


def wrap_text(text, font, max_width):

    lines = []

    current_line = ""

    for word in text.split():

        test_line = word if current_line == "" else current_line + " " + word

        if font.size(test_line)[0] <= max_width:

            current_line = test_line

        else:

            if current_line:
                lines.append(current_line)

            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


# ダメージ文字描画
def draw_damage_texts(screen, damage_texts, font, context):

    cx = context.camera_x
    cy = context.camera_y

    for text in damage_texts:

        damage_surface = font.render(
            str(text["damage"]),
            True,
            (255, 255, 255),
        )

        screen.blit(
            damage_surface,
            (text["x"] - cx, text["y"] - cy),
        )


# 経過時間描画
def draw_timer(screen, font, context):

    # フレーム → 秒
    total_seconds = context.game_timer_sec

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


def draw_game_over(screen, font):

    text = font.render(
        "GAME OVER",
        True,
        (255, 0, 0),
    )

    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(text, rect)


def draw_background(screen, context, background):

    cx = int(context.camera_x)
    cy = int(context.camera_y)

    bg_width = background.get_width()
    bg_height = background.get_height()

    start_x = -(cx % bg_width)
    start_y = -(cy % bg_height)

    for x in range(-1, 2):

        for y in range(-1, 2):

            screen.blit(
                background,
                (
                    start_x + x * bg_width,
                    start_y + y * bg_height,
                ),
            )


def draw_explosions(screen, context):

    for explosion in context.explosions:

        x = explosion["x"] - context.camera_x
        y = explosion["y"] - context.camera_y
        radius = explosion["radius"]

        diameter = radius * 2

        explosion_surface = pygame.Surface(
            (diameter, diameter),
            pygame.SRCALPHA,
        )

        color = explosion.get(
            "color",
            (255, 80, 0, 100),
        )

        pygame.draw.circle(
            explosion_surface,
            color,
            (
                radius,
                radius,
            ),
            radius,
        )

        screen.blit(
            explosion_surface,
            (
                x - radius,
                y - radius,
            ),
        )


def draw_lightning_effects(screen, context):

    cx = context.camera_x
    cy = context.camera_y

    for effect in context.lightning_effects:

        x1 = effect["x1"] - cx
        y1 = effect["y1"] - cy
        x2 = effect["x2"] - cx
        y2 = effect["y2"] - cy

        mid_x = (x1 + x2) / 2 + random.randint(-15, 15)
        mid_y = (y1 + y2) / 2 + random.randint(-15, 15)

        pygame.draw.line(
            screen,
            (180, 220, 255),
            (x1, y1),
            (mid_x, mid_y),
            3,
        )

        pygame.draw.line(
            screen,
            (180, 220, 255),
            (mid_x, mid_y),
            (x2, y2),
            3,
        )


def draw_boss_area_frame(screen, context):

    if context.boss_area is None:
        return

    pygame.draw.rect(
        screen,
        (180, 30, 30),
        (
            0,
            0,
            WIDTH,
            HEIGHT,
        ),
        5,
    )
