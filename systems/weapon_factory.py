from weapon import (
    NormalWeapon,
    RandomWeapon,
    RandomAimWeapon,
    FreezeWeapon,
    SurroundWeapon,
    ChainLightningWeapon,
    MineWeapon,
    HornetNestWeapon,
)

# 武器の登録表
weapon_registry = {
    "normal_weapon": NormalWeapon,
    "random_weapon": RandomWeapon,
    "random_aim_weapon": RandomAimWeapon,
    "freeze_weapon": FreezeWeapon,
    "surround_weapon": SurroundWeapon,
    "chain_lightning_weapon": ChainLightningWeapon,
    "mine_weapon": MineWeapon,
    "hornet_nest_weapon": HornetNestWeapon,
}


def create_weapon(name):

    weapon_class = weapon_registry.get(name)

    if weapon_class is None:
        print("Weapon Not Found")
        return None

    return weapon_class()
