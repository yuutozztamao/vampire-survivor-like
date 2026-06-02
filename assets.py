import pygame

from player import Player
from enemy import *
from weapon import *
from bullet import Bullet
from gem import Gem
from settings import WIDTH, HEIGHT

import pygame


def load_images(paths, width, height=None):

    images = []
    if not height:
        height = width
        # print(paths, width, height)

    for path in paths:

        image = pygame.image.load(path).convert_alpha()

        image = pygame.transform.scale(
            image,
            (width, height),
        )

        images.append(image)

    return images


def load_background(path):

    return pygame.image.load(path).convert()


def load_assets():

    assets = {
        "image": {},
        "sound": {},
        "font": {},
    }

    # 背景は一枚のため、[0]をつける
    assets["image"]["background"] = load_background("images/background.png")

    assets["image"]["player"] = load_images(
        [
            "images/player_0.png",
        ],
        Player.draw_radius * 2,
    )

    assets["image"]["zombie"] = load_images(
        [
            "images/zombie_0.png",
        ],
        Zombie.draw_radius * 2,
    )

    assets["image"]["muscle_zombie"] = load_images(
        [
            "images/muscle_zombie_0.png",
        ],
        MuscleZombie.draw_radius * 2,
    )

    assets["image"]["shooter_zombie"] = load_images(
        [
            "images/shooter_zombie_0.png",
        ],
        ShooterZombie.draw_radius * 2,
    )

    assets["image"]["shooter_zombie_bullet"] = load_images(
        ["images/shooter_zombie_bullet_0.png"], ShooterZombie.bullet_draw_radius * 2
    )

    assets["image"]["boar_zombie"] = load_images(
        ["images/boar_zombie_0.png"], BoarZombie.draw_radius * 2
    )

    assets["image"]["slime_zombie"] = load_images(
        ["images/slime_zombie_0.png"], SlimeZombie.draw_radius * 2
    )

    assets["image"]["bomber_zombie"] = load_images(
        ["images/bomber_zombie_0.png"], BomberZombie.draw_radius * 2
    )

    assets["image"]["normal_bullet"] = load_images(
        [
            "images/normal_bullet_0.png",
        ],
        NormalWeapon.bullet_draw_radius * 2,
    )

    assets["image"]["random_bullet"] = load_images(
        ["images/random_bullet_0.png"],
        RandomWeapon.bullet_draw_radius * 2,
    )

    assets["image"]["random_aim_bullet"] = load_images(
        ["images/random_aim_bullet_0.png"],
        RandomAimWeapon.bullet_draw_radius * 2,
    )

    assets["image"]["freeze_bullet"] = load_images(
        ["images/freeze_bullet_0.png"],
        FreezeWeapon.bullet_draw_radius * 2,
    )

    assets["image"]["surround"] = load_images(
        ["images/surround_area_0.png"], SurroundWeapon.get_draw_radius() * 2
    )

    assets["image"]["gem"] = load_images(
        [
            "images/gem_0.png",
        ],
        Gem.draw_radius * 2,
    )

    return assets


def set_images(assets):

    Player.images = assets["image"]["player"]

    Zombie.images = assets["image"]["zombie"]

    MuscleZombie.images = assets["image"]["muscle_zombie"]

    ShooterZombie.images = assets["image"]["shooter_zombie"]

    ShooterZombie.bullet_images = assets["image"]["shooter_zombie_bullet"]

    BoarZombie.images = assets["image"]["boar_zombie"]

    SlimeZombie.images = assets["image"]["slime_zombie"]

    BomberZombie.images = assets["image"]["bomber_zombie"]

    NormalWeapon.bullet_images = assets["image"]["normal_bullet"]

    RandomWeapon.bullet_images = assets["image"]["random_bullet"]

    RandomAimWeapon.bullet_images = assets["image"]["random_aim_bullet"]

    FreezeWeapon.bullet_images = assets["image"]["freeze_bullet"]

    SurroundWeapon.images = assets["image"]["surround"]

    Gem.images = assets["image"]["gem"]
