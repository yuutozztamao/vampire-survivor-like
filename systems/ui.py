import pygame


def draw_bar(
    screen,
    length,
    value,
    max_value,
    height,
    x,
    y,
    back_color,
    bar_color,
):

    if max_value <= 0:
        return

    pygame.draw.rect(
        screen,
        back_color,
        (x, y, length, height),
    )

    pygame.draw.rect(
        screen,
        bar_color,
        (
            x,
            y,
            length * value / max_value,
            height,
        ),
    )
