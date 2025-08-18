# game/loot.py
import random
from game.config import TILE_SIZE
import game.config as config

def generate_coin_drop(x_px: float, y_px: float, size_px: float) -> list[dict]:
    """
    적 사망 위치 기준 코인 드랍 정보(데이터)만 생성해 돌려준다.
    - Entity 생성은 caller(entity.py)에서 한다 → 순환 import 방지
    반환: [{"value": int, "pos": (px, py)} ...]
    """
    diff = config.itdiff()

    drop_rate = 0.30 + 0.05 * max(0, diff - 1)  # 30% + 단계당 5%
    if random.random() > drop_rate:
        return []

    cnt   = random.randint(1, 1 + diff // 2)   # 1 ~
    value = 1 + (diff // 3)                    # 1, 2, ...

    # 적 중심을 타일 중앙으로 스냅
    cx = int((x_px + size_px / 2) // TILE_SIZE)
    cy = int((y_px + size_px / 2) // TILE_SIZE)
    px = cx * TILE_SIZE + TILE_SIZE * 0.5
    py = cy * TILE_SIZE + TILE_SIZE * 0.5

    return [{"value": value, "pos": (px, py)} for _ in range(cnt)]
