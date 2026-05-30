from utils import is_hit


def player_enemy_collision(player, enemies):

    # 無敵時間中
    if player.invincible_timer > 0:

        return

    for enemy in enemies:

        if is_hit(player, enemy):

            player.health -= enemy.attack_power

            if player.health <= 0:
                return True

            player.invincible_timer = 30

            break

    return False


def gem_collision(player, gems, level_up, need_exp):

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
