import pygame

from player import Player
from enemy import *
from weapon import *
from gem import Gem
from settings import WIDTH, HEIGHT


def load_images(paths, width, height=None):

    images = []

    # height を指定しなかった場合は、width と同じサイズにする
    # 例: width=40, height=None → 40×40 の正方形画像になる
    if not height:
        height = width

    for path in paths:

        # 画像を読み込んで、透過ありの画像として使えるようにする
        image = pygame.image.load(path).convert_alpha()

        # ゲーム内で使うサイズに拡大・縮小する
        image = pygame.transform.scale(
            image,
            (width, height),
        )

        images.append(image)

    return images


def load_background(path):

    image = pygame.image.load(path).convert()

    # 背景画像は、画面サイズに合わせて読み込む
    # settings.py の WIDTH, HEIGHT を変えると、背景サイズも自動で変わる
    image = pygame.transform.scale(
        image,
        (
            WIDTH,
            HEIGHT,
        ),
    )

    return image


def load_assets():

    assets = {
        "image": {
            # 背景画像
            "background": {},

            # プレイヤー本体画像
            "player": {},

            # 敵本体画像
            "enemy": {},

            # 敵が撃つ弾画像
            "enemy_bullet": {},

            # プレイヤーの武器・弾・設置物画像
            "weapon": {},

            # 経験値Gemなどのアイテム画像
            "item": {},

            # 毒泡・凍結雪などの演出画像
            "effect": {},
        },
        "sound": {},
        "font": {},
    }

    images = assets["image"]

    # 画像カテゴリごとの短縮名
    # 例: weapon_images["freeze_bullet"] は assets["image"]["weapon"]["freeze_bullet"] と同じ意味
    background_images = images["background"]
    player_images = images["player"]
    enemy_images = images["enemy"]
    enemy_bullet_images = images["enemy_bullet"]
    weapon_images = images["weapon"]
    item_images = images["item"]
    effect_images = images["effect"]

    # =========================
    # 背景
    # =========================

    background_images["main"] = load_background("images/background.png")

    # =========================
    # プレイヤー
    # =========================

    player_images["main"] = load_images(
        [
            "images/player_0.png",
        ],
        Player.draw_radius * 2,
    )

    # =========================
    # 敵
    # =========================

    enemy_images["zombie"] = load_images(
        [
            "images/zombie_0.png",
        ],
        Zombie.draw_radius * 2,
    )

    enemy_images["muscle_zombie"] = load_images(
        [
            "images/muscle_zombie_0.png",
        ],
        MuscleZombie.draw_radius * 2,
    )

    enemy_images["shooter_zombie"] = load_images(
        [
            "images/shooter_zombie_0.png",
        ],
        ShooterZombie.draw_radius * 2,
    )

    enemy_images["boar_zombie"] = load_images(
        ["images/boar_zombie_0.png"],
        BoarZombie.draw_radius * 2,
    )

    enemy_images["slime_zombie"] = load_images(
        ["images/slime_zombie_0.png"],
        SlimeZombie.draw_radius * 2,
    )

    enemy_images["bomber_zombie"] = load_images(
        ["images/bomber_zombie_0.png"],
        BomberZombie.draw_radius * 2,
    )

    enemy_images["ghost_zombie"] = load_images(
        ["images/ghost_zombie_0.png"],
        GhostZombie.draw_radius * 2,
    )

    enemy_images["shield_zombie"] = load_images(
        ["images/shield_zombie_0.png"],
        ShieldZombie.draw_radius * 2,
    )

    enemy_images["guardian_zombie"] = load_images(
        ["images/guardian_zombie_0.png"],
        GuardianZombie.draw_radius * 2,
    )

    # =========================
    # 敵の弾
    # =========================

    enemy_bullet_images["shooter_zombie"] = load_images(
        ["images/shooter_zombie_bullet_0.png"],
        ShooterZombie.bullet_draw_radius * 2,
    )

    enemy_bullet_images["guardian_zombie"] = load_images(
        ["images/guardian_zombie_bullet_0.png"],
        GuardianZombie.bullet_draw_radius * 2,
    )

    # =========================
    # 武器
    # =========================

    weapon_images["normal_bullet"] = load_images(
        [
            "images/normal_bullet_0.png",
        ],
        NormalWeapon.bullet_draw_radius * 2,
    )

    weapon_images["random_bullet"] = load_images(
        ["images/random_bullet_0.png"],
        RandomWeapon.bullet_draw_radius * 2,
    )

    weapon_images["random_aim_bullet"] = load_images(
        ["images/random_aim_bullet_0.png"],
        RandomAimWeapon.bullet_draw_radius * 2,
    )

    weapon_images["freeze_bullet"] = load_images(
        ["images/freeze_bullet_0.png"],
        FreezeWeapon.bullet_draw_radius * 2,
    )

    weapon_images["balloon_mine"] = load_images(
        ["images/balloon_mine_0.png"],
        MineWeapon.mine_draw_radius * 2,
    )

    weapon_images["hornet_nest_body"] = load_images(
        ["images/hornet_nest_0.png"],
        HornetNestWeapon.draw_radius * 2,
    )

    weapon_images["hornet_bee"] = load_images(
        ["images/hornet_bee_0.png"],
        24,
    )

    weapon_images["surround"] = load_images(
        ["images/surround_area_0.png"],
        SurroundWeapon.get_draw_radius() * 2,
    )

    # =========================
    # アイテム
    # =========================

    item_images["gem"] = load_images(
        [
            "images/gem_0.png",
        ],
        Gem.draw_radius * 2,
    )

    # =========================
    # エフェクト
    # =========================

    effect_images["poison_bubble"] = load_images(
        ["images/poison_bubble_0.png"],
        12,
    )

    effect_images["snowflake"] = load_images(
        ["images/snowflake_0.png"],
        18,
    )

    return assets


def set_images(assets):

    images = assets["image"]

    # 画像カテゴリごとの短縮名
    # 例: enemy_images["zombie"] は assets["image"]["enemy"]["zombie"] と同じ意味
    player_images = images["player"]
    enemy_images = images["enemy"]
    enemy_bullet_images = images["enemy_bullet"]
    weapon_images = images["weapon"]
    item_images = images["item"]
    effect_images = images["effect"]

    # =========================
    # プレイヤー
    # =========================

    Player.images = player_images["main"]

    # =========================
    # 敵
    # =========================

    Zombie.images = enemy_images["zombie"]

    MuscleZombie.images = enemy_images["muscle_zombie"]

    ShooterZombie.images = enemy_images["shooter_zombie"]

    BoarZombie.images = enemy_images["boar_zombie"]

    SlimeZombie.images = enemy_images["slime_zombie"]

    BomberZombie.images = enemy_images["bomber_zombie"]

    GhostZombie.images = enemy_images["ghost_zombie"]

    ShieldZombie.images = enemy_images["shield_zombie"]

    GuardianZombie.images = enemy_images["guardian_zombie"]

    # =========================
    # 敵の弾
    # =========================

    ShooterZombie.bullet_images = enemy_bullet_images["shooter_zombie"]

    GuardianZombie.bullet_images = enemy_bullet_images["guardian_zombie"]

    # =========================
    # 武器
    # =========================

    NormalWeapon.bullet_images = weapon_images["normal_bullet"]

    RandomWeapon.bullet_images = weapon_images["random_bullet"]

    RandomAimWeapon.bullet_images = weapon_images["random_aim_bullet"]

    FreezeWeapon.bullet_images = weapon_images["freeze_bullet"]

    MineWeapon.mine_images = weapon_images["balloon_mine"]

    # HornetNestWeapon は、蜂の巣本体画像を nest_images に入れる
    # images ではないので注意
    HornetNestWeapon.nest_images = weapon_images["hornet_nest_body"]

    # 蜂の巣の周りを飛ぶ蜂画像
    HornetNestWeapon.bee_images = weapon_images["hornet_bee"]

    SurroundWeapon.images = weapon_images["surround"]

    # =========================
    # アイテム
    # =========================

    Gem.images = item_images["gem"]

    # =========================
    # エフェクト
    # =========================

    Enemy.poison_bubble_images = effect_images["poison_bubble"]

    Enemy.freeze_particle_images = effect_images["snowflake"]
