# game/entity.py

import pygame
import math
import time
from game.config import*
from game.collision import check_corner_collision, check_tile_collision
import game.config as config

class Entity:
    def __init__(self, x, y, symbol, entity_type="player"):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.entity_type = entity_type
        if entity_type == "player":
            self.max_hp           = 1000000000000
            self.hp               = self.max_hp
            self.speed            = (TILE_SIZE/50)*2 + (TILE_SIZE/50)*0.25*config.itdiff()
            self.color            = RED
            self.attack_speed     = 0.75 - 0.025*config.itdiff()
            self.damage           = 100
            self.attack_range     = 1
            self.size             = TILE_SIZE * 0.25
            self.last_damage_time = 0
            self.last_attack_time = 0
            self.last_direction   = "down"
        elif entity_type.startswith("B_"):
            attrs = boss_types(config.itdiff()).get(entity_type, boss_types(config.itdiff())["B_a"])
            self.hp               = attrs["hp"]
            self.speed            = attrs["speed"]
            self.color            = attrs["color"]
            self.attack_speed     = attrs["attack_speed"]
            self.damage           = attrs["damage"]
            self.size             = attrs["size"]
            self.attack_type      = attrs["attack_type"]
            self.last_attack_time = 0
        elif entity_type == "item":
            self.entity_type = 'item'
            self.size = TILE_SIZE * 0.2
            self.color = BLACK
        else:
            attrs = enemy_types(config.itdiff()).get(entity_type, enemy_types(config.itdiff())["a"])
            self.hp               = attrs["hp"]
            self.speed            = attrs["speed"]
            self.color            = attrs["color"]
            self.attack_speed     = attrs["attack_speed"]
            self.damage           = attrs["damage"]
            self.size             = attrs["size"]
            self.last_attack_time = 0
            self.attack_type      = attrs["attack_type"]

    def draw(self):
        screen = pygame.display.get_surface()
        rect = pygame.Rect(int(self.x), int(self.y), int(self.size), int(self.size))

        # 아이템: 기존 스타일 유지 (필요 없다면 이 블록 삭제)
        if  self.entity_type == "item":
            pygame.draw.rect(screen, BLACK, (self.x + TILE_SIZE*0.5 - self.size*0.5, self.y+ TILE_SIZE*0.5 - self.size*0.5, self.size, self.size))
            return

        # 플레이어: 채움 유지
        if getattr(self, "entity_type", "") == "player":
            pygame.draw.rect(screen, self.color, rect)
            return

        # 적/보스: 채우기 없이 테두리
        pygame.draw.rect(screen, self.color, rect, 2)

        # 중앙 텍스트: attack_type + damage(damge)
        pre = getattr(self, "attack_type", None)
        amt = getattr(self, "damge", None)
        if amt is None:
            amt = getattr(self, "damage", None)

        if pre and (amt is not None):
            try:
                amt_i = int(amt)
            except (TypeError, ValueError):
                amt_i = amt
            label = f"{pre} {amt_i}"

            font = pygame.font.SysFont(None, int(self.size * 0.6), bold=True)
            text = font.render(label, True, self.color)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
    
    def draw_attack_range(self):
        # (선택) 공격 범위 원을 그립니다. 디버그용으로만 사용하세요.
        center = (int(self.x + self.size/2), int(self.y + self.size/2))
        pygame.draw.circle(pygame.display.get_surface(), (255, 255, 0),
                           center, TILE_SIZE, 1)


    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def move_towards(self, target_x, target_y, tilemap, stop_distance=10, enemies=None):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist <= stop_distance:
            return
            # 정규화
        dx_norm, dy_norm = dx / dist, dy / dist

        # X축 이동 시 맵 충돌 검사
        new_x = self.x + dx_norm * self.speed
        if not check_tile_collision(new_x, self.y, self.size, tilemap):
            self.x = new_x

        # Y축 이동 시 맵 충돌 검사
        new_y = self.y + dy_norm * self.speed
        if not check_tile_collision(self.x, new_y, self.size, tilemap):
            self.y = new_y

        # 다른 적들과의 충돌 방지 (살짝 밀어내기)
        if enemies:
            for other in enemies:
                if other is not self and check_corner_collision(self, other):
                    ox = (self.get_rect().centerx - other.get_rect().centerx) / 2
                    oy = (self.get_rect().centery - other.get_rect().centery) / 2
                    self.x += ox * 0.1
                    self.y += oy * 0.1

    def attack(self, player):
        now = time.time()
        if now - self.last_attack_time < self.attack_speed:
            return

        # 중심거리 + 마진
        cx, cy = self.x + self.size/2, self.y + self.size/2
        px, py = player.x + player.size/2, player.y + player.size/2
        center_dist = math.hypot(cx - px, cy - py)
        contact_threshold = (self.size + player.size)/2 + config.CONTACT_MARGIN_PX
        near_contact = center_dist <= contact_threshold

        # 직전 프레임의 접촉 그레이스
        grace = (now - getattr(self, "last_touch_time", 0)) <= config.CONTACT_GRACE_SEC

        if (near_contact or grace) and (now - player.last_damage_time) >= 1:
            player.hp -= self.damage
            player.last_damage_time = now

        # 쿨타임 갱신(명중 여부와 무관하게 시도 간격 제한)
        self.last_attack_time = now


    def attack_enemies(self, enemies, bosses=None):
        now = time.time()
        if now - self.last_attack_time < self.attack_speed:
            return

        attack_range = self.attack_range * TILE_SIZE
        attack_width = TILE_SIZE * 0.8  # 사각형 너비 (좌우 허용 범위)
        px = self.x + self.size / 2
        py = self.y + self.size / 2

        targets = []
        if enemies:
            targets.extend(enemies)
        if bosses:
            targets.extend(bosses)

        for target in targets:
            
            ex = target.x + target.size / 2
            ey = target.y + target.size / 2

            in_range = False

            if self.last_direction == "up":
                if (abs(ex - px) <= attack_width / 2 and
                    py - attack_range <= ey < py):
                    in_range = True
            elif self.last_direction == "down":
                if (abs(ex - px) <= attack_width / 2 and
                    py < ey <= py + attack_range):
                    in_range = True
            elif self.last_direction == "left":
                if (abs(ey - py) <= attack_width / 2 and
                    px - attack_range <= ex < px):
                    in_range = True
            elif self.last_direction == "right":
                if (abs(ey - py) <= attack_width / 2 and
                    px < ex <= px + attack_range):
                    in_range = True

            if in_range:
                target.hp -= self.damage
                print(f"[공격] {target.symbol}에게 {self.damage} 데미지")
                self.last_attack_time = now  # 타격했을 때만 쿨타임 초기화

        # 죽은 적 제거
        if enemies:
            enemies[:] = [e for e in enemies if e.hp > 0]
        if bosses:
            bosses[:] = [b for b in bosses if b.hp > 0]


def draw_attack_area(self):
    """플레이어의 전방 공격 범위를 시각적으로 사각형으로 표시합니다."""
    if self.entity_type != "player":
        return

    attack_range = self.attack_range * TILE_SIZE
    attack_width = TILE_SIZE * 0.8
    px = self.x + self.size / 2
    py = self.y + self.size / 2

    screen = pygame.display.get_surface()

    if self.last_direction == "up":
        rect = pygame.Rect(
            px - attack_width/2,
            py - attack_range,
            attack_width,
            attack_range
        )
    elif self.last_direction == "down":
        rect = pygame.Rect(
            px - attack_width/2,
            py,
            attack_width,
            attack_range
        )
    elif self.last_direction == "left":
        rect = pygame.Rect(
            px - attack_range,
            py - attack_width/2,
            attack_range,
            attack_width
        )
    elif self.last_direction == "right":
        rect = pygame.Rect(
            px,
            py - attack_width/2,
            attack_range,
            attack_width
        )
    else:
        return

    pygame.draw.rect(screen, YELLOW, rect, 2)
