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


def draw_entity_health_bar(screen, context, obj):
    
    if not obj.health_bar_visible:
        return

    cx = context.camera_x
    cy = context.camera_y

    length = obj.health_bar_length
    value = obj.health_bar_value
    max_value = obj.health_bar_max_value
    height = obj.health_bar_height

    x = obj.x - length / 2 - cx
    y = obj.health_bar_y - cy

    draw_bar(
        screen,
        length,
        value,
        max_value,
        height,
        x,
        y,
        obj.health_bar_back_color,
        obj.health_bar_color,
    )

