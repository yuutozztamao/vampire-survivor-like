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
from systems.spawning import *
from systems.level_up import *
from systems.drawing import *


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
        bullets,
        gems,
        damage_texts,
        keys,
    ):

        self.player = player
        self.enemies = enemies
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

    # 武器
    weapons = []

    normal_weapon = NormalWeapon()
    weapons.append(normal_weapon)
    normal_weapon.unlocked = True

    random_weapon = RandomWeapon()

    random_aim_weapon = RandomAimWeapon()

    surround_weapon = SurroundWeapon()
    weapons.append(surround_weapon)
    surround_weapon.unlocked = True

    # レベルアップ処理
    damage_up = PowerUp("ALL DAMAGE UP", lambda: add_param(player, "attack_rate", 0.2))
    speed_up = PowerUp("SPEED UP", lambda: add_param(player, "speed", 1))

    # レベルアップの選択肢のリスト
    level_up_list = {
        damage_up,
        speed_up,
        normal_weapon,
        random_weapon,
        random_aim_weapon,
        surround_weapon,
    }

    # 敵リスト
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

    # 敵
    enemies = []

    next_enemy_id = 0

    # 弾
    bullets = []

    # ジェム
    gems = []

    level_up_choices = []

    level_up = False

    # ダメージ文字
    damage_texts = []

    context = GameContext(player, enemies, bullets, gems, damage_texts, None)

    # レベルアップに必要なexp
    need_exp = 10

    running = True

    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 40)

    while running:

        # イベント
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # レベルアップ
            if level_up:

                level_up = level_up_select(
                    event,
                    level_up,
                    weapons,
                    level_up_choices,
                    level_up_list,
                )

        # キー入力
        keys = pygame.key.get_pressed()
        context.keys = keys

        if not level_up:

            # 更新
            player.update(context)

            for enemy in enemies:
                enemy.update(context)

            enemy_separate(enemies)

            for bullet in bullets:
                bullet.update(context)

            bullets[:] = [bullet for bullet in bullets if not bullet.dead]

            update_damage_texts(damage_texts)

            level_up, need_exp = gem_collision(player, gems, level_up, need_exp)

            if level_up:

                level_up_choices = get_level_up_choices(level_up_list)

            for weapon in weapons:

                weapon.update(context)

            next_enemy_id = enemy_spawn(enemies, enemy_list, game_timer, next_enemy_id)

            # ゲームオーバー
            if player_enemy_collision(player, enemies):

                print("GAME OVER")

                running = False

        # 描画
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

            draw_level_up(screen, font, level_up_choices)

        pygame.display.update()

        game_timer += 1

        clock.tick(60)

    pygame.quit()


# 実行
if __name__ == "__main__":
    main()
