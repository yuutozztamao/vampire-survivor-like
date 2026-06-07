# =========================
# 状態異常
# =========================

# 凍結
def apply_frozen(enemy, duration=120, rate=0.5):
    enemy.frozen_timer = duration
    enemy.frozen_rate = rate

# 毒
def apply_poison(
    enemy,
    duration=180,
):
    enemy.poison_timer = duration
