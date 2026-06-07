from utils import is_hit, enemy_knockback
from systems.condition import apply_frozen
import math

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


def bullet_shield_collision(context):

    for bullet in context.bullets:

        hit_shield = damage_shields_in_circle(
            context,
            bullet.x,
            bullet.y,
            bullet.hit_radius,
            bullet.attack_power,
        )

        if hit_shield:

            bullet.dead = True

            return


def bullet_enemy_collision(context):

    bullet_shield_collision(context)

    for bullet in context.bullets:
        if bullet.dead:
            continue
        
        for enemy in context.enemies:

            if (
                is_hit(bullet, enemy)
                and enemy.id not in bullet.hit_enemies
                and not getattr(enemy, "ghost", False)
            ):

                enemy.take_damage(context, bullet.attack_power)

                enemy_knockback(enemy, bullet)

                bullet.hit_enemies.add(enemy.id)

                if bullet.freeze:
                    apply_frozen(enemy)

                if not bullet.through:
                    bullet.dead = True
                    return

                bullet.dead = False


def mine_enemy_collision(context):

    mines = context.mines
    enemies = context.enemies

    for mine in mines[:]:

        # すでに爆発準備中なら無視
        if mine.exploding:
            continue

        for enemy in enemies:

            if not is_hit(mine, enemy):
                continue

            mine.exploding = True

            break


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


def damage_shields_in_circle(
    context,
    x,
    y,
    radius,
    attack_power,
):

    hit_shield = False

    for enemy in context.enemies:

        if not getattr(enemy, "shield_active", False):
            continue

        distance = math.hypot(
            x - enemy.x,
            y - enemy.y,
        )

        if distance > radius + enemy.shield_radius:
            continue

        enemy.take_shield_damage(
            context,
            attack_power,
        )

        hit_shield = True

    return hit_shield


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
