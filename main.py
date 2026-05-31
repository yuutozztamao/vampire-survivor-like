import pygame
import random
import math

from assets import set_images, load_assets
from settings import WIDTH, HEIGHT
from player import Player
from enemy import *
from weapon import *
from gem import Gem
from utils import enemy_separate
from systems.collision import *
from systems.spawning import enemy_list, enemy_spawn
from systems.level_up import *
from systems.drawing import *
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


class GameContext:

    def __init__(
        self,
        player,
        enemies,
        weapons,
        bullets,
        gems,
        damage_texts,
        keys=None,
    ):

        self.player = player
        self.enemies = enemies
        self.weapons = weapons
        self.bullets = bullets
        self.gems = gems
        self.damage_texts = damage_texts
        self.keys = keys


# メイン処理
def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Vampire Survivor Like")

    game_timer = 0

    # 画像のロード
    assets = load_assets()
    set_images(assets)

    # プレイヤー
    player = Player()

    weapons = []

    initial_weapons = ["normal_weapon", "surround_weapon"]

    for name in initial_weapons:
        w = create_weapon(name)
        w.unlocked = True
        weapons.append(w)

    enemies = []
    bullets = []
    gems = []

    next_enemy_id = 0

    level_up_choices = []

    level_up = False

    # ダメージ文字
    damage_texts = []

    context = GameContext(player, enemies, weapons, bullets, gems, damage_texts)

    # レベルアップに必要なexp
    need_exp = 10

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

            if level_up:

                result = level_up_select(
                    event,
                    level_up_choices,
                    player,
                    weapons,
                )

                if result is not None:
                    level_up = False

        # キー入力
        keys = pygame.key.get_pressed()
        context.keys = keys

        if not level_up:

            # =========================
            # 更新処理
            # =========================

            player.update(context)

            for enemy in enemies:
                enemy.update(context)

            enemy_separate(enemies)

            for bullet in bullets:
                bullet.update(context)

            bullet_enemy_collision(context)

            bullets[:] = [bullet for bullet in bullets if not bullet.dead]

            update_damage_texts(damage_texts)

            level_up, need_exp = gem_collision(player, gems, level_up, need_exp)

            if level_up:

                current_pool = build_level_up_pool(
                    level_up_pool,
                    weapons,
                )

                level_up_choices = get_level_up_choices(current_pool)

            for weapon in weapons:

                weapon.update(context)

            next_enemy_id = enemy_spawn(enemies, enemy_list, game_timer, next_enemy_id)

            # ゲームオーバー
            if player_enemy_collision(player, enemies):

                print("GAME OVER")

                running = False

            game_timer += 1

        # =========================
        # 描画処理
        # =========================

        screen.fill((0, 0, 0))

        player.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

        for gem in gems:
            gem.draw(screen)

        draw_exp_bar(screen, player, need_exp)

        for weapon in weapons:

            if isinstance(weapon, DamageAreaWeapon):
                weapon.draw(screen, player)

        draw_damage_texts(
            screen,
            damage_texts,
            font,
        )

        draw_timer(screen, font, game_timer)

        if level_up:

            draw_level_up(
                screen,
                font,
                level_up_choices,
                weapons,
            )

        pygame.display.update()

        clock.tick(60)

    pygame.quit()


# 実行
if __name__ == "__main__":
    main()
