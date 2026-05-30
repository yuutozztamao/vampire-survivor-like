import pygame
import random


class PowerUp:

    def __init__(self, name, effect):

        self.name = name
        self.effect = effect

    def level_up(self, weapons, level_up_list):

        self.effect()


def level_up_select(
    event,
    level_up,
    weapons,
    level_up_choices,
    level_up_list,
):

    if event.type != pygame.KEYDOWN:
        return level_up

    key_map = {
        pygame.K_1: 0,
        pygame.K_2: 1,
        pygame.K_3: 2,
    }

    if event.key not in key_map:
        return level_up

    index = key_map[event.key]

    if index >= len(level_up_choices):
        return level_up

    choice = level_up_choices[index]

    choice.level_up(weapons, level_up_list)

    return False


def get_level_up_choices(level_up_list):

    count = min(3, len(level_up_list))

    level_up_choices = random.sample(list(level_up_list), count)

    return level_up_choices


def add_param(obj, param, value, minimum=None):

    new_value = getattr(obj, param) + value

    if minimum is not None:
        new_value = max(minimum, new_value)

    setattr(obj, param, new_value)
