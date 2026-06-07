# ダメージ文字・爆発・雷など、時間で消えるエフェクトを更新するファイル
# 描画は systems/drawing.py、更新はこのファイルで担当する

def update_damage_texts(damage_texts):

    for text in damage_texts[:]:

        # 上に移動
        text["y"] -= 1

        # 時間減少
        text["timer"] -= 1

        # 時間切れで削除
        if text["timer"] <= 0:
            damage_texts.remove(text)


def update_timed_effects(effects):

    for effect in effects[:]:

        effect["timer"] -= 1

        if effect["timer"] <= 0:
            effects.remove(effect)


def update_explosions(explosions):

    update_timed_effects(explosions)


def update_lightning_effects(lightning_effects):

    update_timed_effects(lightning_effects)


def update_effects(context):

    update_damage_texts(context.damage_texts)

    update_explosions(context.explosions)

    update_lightning_effects(context.lightning_effects)


def add_explosion_effect(
    context,
    x,
    y,
    radius,
    timer=20,
    color=None,
):

    # 爆発エフェクトを追加する
    # color を指定しない場合は、drawing.py 側の通常色で描画される
    effect = {
        "x": x,
        "y": y,
        "radius": radius,
        "timer": timer,
    }

    if color is not None:
        effect["color"] = color

    context.explosions.append(effect)


def add_lightning_effect(
    context,
    x1,
    y1,
    x2,
    y2,
    timer=8,
):

    # 雷エフェクトを追加する
    # x1, y1 が始点、x2, y2 が終点
    context.lightning_effects.append(
        {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "timer": timer,
        }
    )
