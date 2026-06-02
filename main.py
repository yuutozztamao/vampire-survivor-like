import pygame
import random
import math

from assets import set_images, load_assets
from settings import WIDTH, HEIGHT
from player import Player
from weapon import *
from utils import enemy_separate
from systems.collision import (
    player_enemy_collision,
    bullet_enemy_collision,
    enemy_bullet_collision,
    gem_collision,
)
from systems.spawning import enemy_spawn
from systems.level_up import get_level_up_choices, level_up_select, build_level_up_pool
from systems.drawing import (
    draw_timer,
    draw_damage_texts,
    draw_level_up,
    draw_exp_bar,
    draw_game_over,
    draw_background,
    draw_explosions,
)
from systems.weapon_factory import create_weapon


def update_damage_texts(damage_texts):

    for text in damage_texts[:]:

        # 上に移動
        text["y"] -= 1

        # 時間減少
        text["timer"] -= 1

        # 時間切れで削除
        if text["timer"] <= 0:
            damage_texts.remove(text)


def update_explosions(explosions):

    for explosion in explosions[:]:

        explosion["timer"] -= 1

        if explosion["timer"] <= 0:
            explosions.remove(explosion)


class GameContext:

    def __init__(
        self,
        player,
        keys=None,
    ):

        self.player = player
        self.enemies = []
        self.weapons = []
        self.bullets = []
        self.enemy_bullets = []
        self.gems = []
        self.damage_texts = []
        self.explosions = []
        self.keys = keys
        self.camera_x = 0
        self.camera_y = 0
        self.level_up = False
        self.level_up_choices = []
        self.need_exp = 10
        self.game_timer = 0
        self.game_over = False
        self.next_enemy_id = 0


# メイン処理
def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Vampire Survivor Like")

    # 画像のロード
    assets = load_assets()
    set_images(assets)
    background = assets["image"]["background"]

    player = Player()
    context = GameContext(player)

    initial_weapons = ["normal_weapon"]

    for name in initial_weapons:
        w = create_weapon(name)
        w.unlocked = True
        context.weapons.append(w)

    running = True

    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 40)

    while running:

        # =========================
        # イベント処理
        # =========================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if context.level_up:

                result = level_up_select(event, context)

                if result is not None:
                    context.level_up = False

        # キー入力
        keys = pygame.key.get_pressed()
        context.keys = keys

        if not context.level_up and not context.game_over:

            # =========================
            # 更新処理
            # =========================

            player.update(context)

            # カメラはプレイヤーを追従する
            context.camera_x = player.x - WIDTH // 2
            context.camera_y = player.y - HEIGHT // 2

            for enemy in context.enemies:
                enemy.update(context)

            enemy_separate(context.enemies)

            for bullet in context.bullets:
                bullet.update(context)

            bullet_enemy_collision(context)

            context.bullets[:] = [
                bullet for bullet in context.bullets if not bullet.dead
            ]

            for enemy_bullet in context.enemy_bullets:
                enemy_bullet.update(context)

            enemy_bullet_collision(context)

            context.enemy_bullets[:] = [
                bullet for bullet in context.enemy_bullets if not bullet.dead
            ]

            update_damage_texts(context.damage_texts)
            update_explosions(context.explosions)

            context.level_up, context.need_exp = gem_collision(context)

            if context.level_up:

                current_pool = build_level_up_pool(
                    context.weapons,
                )

                context.level_up_choices = get_level_up_choices(current_pool)

            for weapon in context.weapons:

                weapon.update(context)

            context.next_enemy_id = enemy_spawn(context.enemies, context)

            # ゲームオーバー
            player_enemy_collision(context)

            context.game_timer += 1

        # =========================
        # 描画処理
        # =========================

        draw_background(
            screen,
            context,
            background,
        )

        player.draw(screen, context)

        for enemy in context.enemies:
            enemy.draw(screen, context)

        for bullet in context.bullets:
            bullet.draw(screen, context)

        for enemy_bullet in context.enemy_bullets:
            enemy_bullet.draw(screen, context)

        draw_explosions(screen, context)

        for gem in context.gems:
            gem.draw(screen, context)

        draw_exp_bar(screen, context)

        for weapon in context.weapons:

            if isinstance(weapon, DamageAreaWeapon):
                weapon.draw(screen, context)

        draw_damage_texts(screen, context.damage_texts, font, context)

        for gem in context.gems:

            gem.update(context)

        if context.level_up:

            draw_level_up(screen, font, context)

        draw_timer(screen, font, context)

        if context.game_over:

            draw_game_over(screen, font)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()


# 実行
if __name__ == "__main__":
    main()
