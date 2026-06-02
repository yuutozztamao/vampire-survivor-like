from utils import is_hit, enemy_knockback
from systems.condition import *


def player_enemy_collision(context):

    player = context.player
    enemies = context.enemies

    # 無敵時間中
    if player.invincible_timer > 0:

        return

    for enemy in enemies:

        if is_hit(player, enemy):

            player.take_damage(
                context,
                enemy.attack_power,
            )

            break


def bullet_enemy_collision(context):

    for bullet in context.bullets:
        for enemy in context.enemies:

            if is_hit(bullet, enemy) and enemy.id not in bullet.hit_enemies:

                enemy.take_damage(context, bullet.attack_power)

                enemy_knockback(enemy, bullet)

                bullet.hit_enemies.add(enemy.id)

                if bullet.freeze:
                    apply_frozen(enemy)

                if not bullet.through:
                    bullet.dead = True
                    return

                bullet.dead = False


def enemy_bullet_collision(context):

    player = context.player

    # 無敵時間中
    if player.invincible_timer > 0:

        return

    for bullet in context.enemy_bullets[:]:

        if not is_hit(player, bullet):
            continue

        player.take_damage(
            context,
            bullet.attack_power,
        )

        bullet.dead = True

        break


def gem_collision(context):

    player = context.player
    gems = context.gems
    level_up = context.level_up
    need_exp = context.need_exp

    for gem in gems[:]:

        if is_hit(player, gem):

            player.exp += gem.exp

            gems.remove(gem)

            # レベルアップ
            if player.exp >= need_exp:

                player.lv += 1

                # 余った経験値を残す
                player.exp -= need_exp

                need_exp = int(need_exp * 1.5)

                level_up = True

    return level_up, need_exp
