import pygame

from assets import set_images, load_assets
from settings import WIDTH, HEIGHT
from player import Player
from weapon import DamageAreaWeapon
from utils import enemy_separate
from systems.collision import (
    player_enemy_collision,
    bullet_enemy_collision,
    mine_enemy_collision,
    enemy_bullet_collision,
    gem_collision,
)
from systems.spawning import enemy_spawn
from systems.effect import update_effects
from systems.level_up import get_level_up_choices, level_up_select, build_level_up_pool
from systems.drawing import (
    draw_timer,
    draw_damage_texts,
    draw_level_up,
    draw_exp_bar,
    draw_game_over,
    draw_background,
    draw_explosions,
    draw_lightning_effects,
    draw_boss_area_frame
)
from systems.weapon_factory import create_weapon

# ゲーム中に共有したいデータをまとめて持つクラス
# player, enemies, bullets などを context にまとめることで、
# 関数に渡す引数を少なくできる
class GameContext:

    def __init__(
        self,
        player,
        keys=None,
    ):

        # プレイヤー
        self.player = player

        # ゲーム内オブジェクト
        self.enemies = []
        self.weapons = []
        self.bullets = []
        self.mines = []
        self.hornet_nests = []
        self.enemy_bullets = []
        self.gems = []

        # 表示エフェクト
        self.damage_texts = []
        self.explosions = []
        self.lightning_effects = []

        # 入力
        self.keys = keys

        # カメラ
        self.camera_x = 0
        self.camera_y = 0
        self.camera_unlocking = False
        self.camera_unlock_speed = 0.06

        # レベルアップ
        self.level_up = False
        self.level_up_choices = []
        self.need_exp = 10

        # タイマー
        self.game_timer = 0
        self.spawn_timer = 0

        # ゲーム状態
        self.game_over = False
        self.next_enemy_id = 0

        # ボス関連
        self.boss = None
        self.boss_area = None

    # game_timer はフレーム数で管理しているので、秒に変換して使う
    @property
    def game_timer_sec(self):
        return self.game_timer // 60

    # spawn_timer もフレーム数で管理しているので、秒に変換して使う
    # ボス中は spawn_timer を止めるので、通常敵の出現タイミング調整に使う
    @property
    def spawn_timer_sec(self):
        return self.spawn_timer // 60

    # ボスが現在生きているかどうか
    # boss が None ではなく、かつ enemies の中に残っていればボス出現中
    @property
    def boss_active(self):

        return self.boss is not None and self.boss in self.enemies


def remove_dead_objects(objects):

    objects[:] = [obj for obj in objects if not obj.dead]


def update_player_bullets(context):

    for bullet in context.bullets:
        bullet.update(context)

    bullet_enemy_collision(context)

    remove_dead_objects(context.bullets)


def update_mines(context):

    for mine in context.mines:
        mine.update(context)

    mine_enemy_collision(context)

    remove_dead_objects(context.mines)


def update_hornet_nests(context):

    for hornet_nest in context.hornet_nests:
        hornet_nest.update(context)

    remove_dead_objects(context.hornet_nests)


def update_enemy_bullets(context):

    for enemy_bullet in context.enemy_bullets:
        enemy_bullet.update(context)

    enemy_bullet_collision(context)

    remove_dead_objects(context.enemy_bullets)


def update_gems(context):

    for gem in context.gems:
        gem.update(context)

    context.level_up, context.need_exp = gem_collision(context)

    if context.level_up:

        current_pool = build_level_up_pool(
            context.weapons,
        )

        context.level_up_choices = get_level_up_choices(current_pool)


def update_weapons(context):

    for weapon in context.weapons:

        weapon.update(context)


def update_enemies(context):

    for enemy in context.enemies:
        enemy.shield_count = 0

    for enemy in context.enemies:
        enemy.update(context)

    enemy_separate(context.enemies)


def clamp_player_to_boss_area(context):

    if context.boss_area is None:
        return

    player = context.player
    area = context.boss_area

    player.x = max(
        area["left"] + player.hit_radius,
        min(
            player.x,
            area["right"] - player.hit_radius,
        ),
    )

    player.y = max(
        area["top"] + player.hit_radius,
        min(
            player.y,
            area["bottom"] - player.hit_radius,
        ),
    )


def lock_camera_to_boss_area(context):

    if context.boss_area is None:
        return

    area = context.boss_area

    context.camera_x = area["left"]
    context.camera_y = area["top"]


def update_normal_camera(context):

    player = context.player

    target_camera_x = player.x - WIDTH // 2
    target_camera_y = player.y - HEIGHT // 2

    if context.camera_unlocking:

        context.camera_x += (
            target_camera_x - context.camera_x
        ) * context.camera_unlock_speed

        context.camera_y += (
            target_camera_y - context.camera_y
        ) * context.camera_unlock_speed

        if (
            abs(target_camera_x - context.camera_x) < 1
            and abs(target_camera_y - context.camera_y) < 1
        ):

            context.camera_x = target_camera_x
            context.camera_y = target_camera_y
            context.camera_unlocking = False

    else:

        context.camera_x = target_camera_x
        context.camera_y = target_camera_y


def update_player(context):

    player = context.player

    player.update(context)

    if context.boss_area:

        clamp_player_to_boss_area(context)

        lock_camera_to_boss_area(context)

    else:

        update_normal_camera(context)


def clear_boss_state(context):

    context.boss = None
    context.boss_area = None

    # ボス撃破後、固定されていたカメラをプレイヤー中心へなめらかに戻す
    context.camera_unlocking = True


def update_boss_state(context):

    if context.boss is None:
        return

    if context.boss_active:
        return

    clear_boss_state(context)


def update_enemy_spawn(context):

    context.next_enemy_id = enemy_spawn(context)


def update_game_timers(context):

    context.game_timer += 1

    if not context.boss_active:

        context.spawn_timer += 1


# 敵スポーンとゲーム内タイマーを更新する
def update_spawn_and_timers(context):

    update_enemy_spawn(context)

    update_game_timers(context)


def update_game(context):

    # プレイヤー・敵の更新
    update_player(context)

    update_enemies(context)

    # プレイヤーの攻撃更新
    update_player_bullets(context)

    update_mines(context)

    update_hornet_nests(context)

    # 敵の攻撃更新
    update_enemy_bullets(context)

    # ダメージ文字・爆発・雷などのエフェクト更新
    update_effects(context)

    # 経験値Gem更新
    update_gems(context)

    # 武器の発射・発動更新
    update_weapons(context)

    # プレイヤーと敵の接触判定
    player_enemy_collision(context)

    # スポーン・タイマー
    update_spawn_and_timers(context)

    # ボス撃破後の状態更新
    update_boss_state(context)


def draw_game(screen, font, context, background):

    # 背景
    draw_background(
        screen,
        context,
        background,
    )

    # プレイヤー・敵
    context.player.draw(screen, context)

    for enemy in context.enemies:
        enemy.draw(screen, context)

    # プレイヤーの攻撃
    for bullet in context.bullets:
        bullet.draw(screen, context)

    for mine in context.mines:
        mine.draw(screen, context)

    for hornet_nest in context.hornet_nests:
        hornet_nest.draw(screen, context)

    # 攻撃エフェクト
    draw_explosions(screen, context)

    draw_lightning_effects(screen, context)

    # アイテム
    for gem in context.gems:
        gem.draw(screen, context)

    # 敵の攻撃
    for enemy_bullet in context.enemy_bullets:
        enemy_bullet.draw(screen, context)

    # UI
    draw_exp_bar(screen, context)

    for weapon in context.weapons:

        if isinstance(weapon, DamageAreaWeapon):
            weapon.draw(screen, context)

    draw_damage_texts(
        screen,
        context.damage_texts,
        font,
        context,
    )

    draw_boss_area_frame(
        screen,
        context,
    )

    if context.level_up:

        draw_level_up(
            screen,
            font,
            context,
        )

    draw_timer(
        screen,
        font,
        context,
    )

    if context.game_over:

        draw_game_over(
            screen,
            font,
        )


def handle_events(context):

    running = True

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if context.level_up:

            result = level_up_select(event, context)

            if result is not None:
                context.level_up = False

    return running


# メイン処理
def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Vampire Survivor Like")

    # 画像・音・フォントなどの素材を読み込む
    assets = load_assets()

    # 読み込んだ画像を、Player や Enemy などの各クラスにセットする
    set_images(assets)

    # 背景画像を取り出す
    background = assets["image"]["background"]["main"]

    player = Player()
    context = GameContext(player)

    initial_weapons = ["chain_lightning_weapon"]

    for name in initial_weapons:
        w = create_weapon(name)
        context.weapons.append(w)

    running = True

    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 40)

    while running:

        # =========================
        # イベント処理
        # =========================

        running = handle_events(context)

        # キー入力
        keys = pygame.key.get_pressed()
        context.keys = keys

        # =========================
        # 更新処理
        # =========================

        if not context.level_up and not context.game_over:

            update_game(context)

        # =========================
        # 描画処理
        # =========================

        draw_game(
            screen,
            font,
            context,
            background,
        )

        pygame.display.update()

        clock.tick(60)

    pygame.quit()


# 実行
if __name__ == "__main__":
    main()
