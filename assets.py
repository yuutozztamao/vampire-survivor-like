import pygame

from player import Player
from enemy import *
from weapon import *
from bullet import Bullet
from gem import Gem

import pygame


def load_images(paths, radius):

    images = []

    for path in paths:

        image = pygame.image.load(path).convert_alpha()

        image = pygame.transform.scale(
            image,
            (radius * 2, radius * 2),
        )

        images.append(image)

    return images


def load_assets():

    assets = {
        "image": {},
        "sound": {},
        "font": {},
    }

    assets["image"]["player"] = load_images(
        [
            "images/player_0.png",
        ],
        Player.draw_radius,
    )

    assets["image"]["zombie"] = load_images(
        [
            "images/zombie_0.png",
        ],
        Zombie.draw_radius,
    )

    assets["image"]["muscle_zombie"] = load_images(
        [
            "images/muscle_zombie_0.png",
        ],
        MuscleZombie.draw_radius,
    )

    assets["image"]["normal_bullet"] = load_images(
        [
            "images/normal_bullet_0.png",
        ],
        NormalWeapon.bullet_draw_radius,
    )

    assets["image"]["random_bullet"] = load_images(
        ["images/random_bullet_0.png"],
        RandomWeapon.bullet_draw_radius,
    )

    assets["image"]["random_aim_bullet"] = load_images(
        ["images/random_aim_bullet_0.png"],
        RandomAimWeapon.bullet_draw_radius,
    )

    assets["image"]["freeze_bullet"] = load_images(
        ["images/freeze_bullet_0.png"],
        FreezeWeapon.bullet_draw_radius,
    )

    assets["image"]["surround"] = load_images(
        ["images/surround_area_0.png"], SurroundWeapon.get_draw_radius()
    )

    assets["image"]["gem"] = load_images(
        [
            "images/gem_0.png",
        ],
        Gem.draw_radius,
    )

    return assets


def set_images(assets):

    Player.images = assets["image"]["player"]

    Zombie.images = assets["image"]["zombie"]

    MuscleZombie.images = assets["image"]["muscle_zombie"]

    NormalWeapon.bullet_images = assets["image"]["normal_bullet"]

    RandomWeapon.bullet_images = assets["image"]["random_bullet"]

    RandomAimWeapon.bullet_images = assets["image"]["random_aim_bullet"]

    FreezeWeapon.bullet_images = assets["image"]["freeze_bullet"]

    SurroundWeapon.images = assets["image"]["surround"]

    Gem.images = assets["image"]["gem"]
