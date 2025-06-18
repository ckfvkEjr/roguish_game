# game/entity.py

import pygame
import math
import time
from game.config import TILE_SIZE, RED, BLACK, diff, enemy_types, boss_types
from game.collision import check_corner_collision, check_tile_collision
import game.config as config

class Entity:
    def __init__(self, x, y, symbol, entity_type="player"):
        self.x = x
        self.y = y
        self.symbol = symbol

        if entity_type == "player":
            self.hp               = 100
            self.speed            = (TILE_SIZE/50)*2 + (TILE_SIZE/50)*0.25*config.itdiff()
            self.color            = RED
            self.attack_speed     = 0.75 - 0.025*config.itdiff()
            self.damage           = 5
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
            self.last_attack_time = 0
        else:
            attrs = enemy_types(config.itdiff()).get(entity_type, enemy_types(config.itdiff())["a"])
            self.hp               = attrs["hp"]
            self.speed            = attrs["speed"]
            self.color            = attrs["color"]
            self.attack_speed     = attrs["attack_speed"]
            self.damage           = attrs["damage"]
            self.size             = attrs["size"]
            self.last_attack_time = 0

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color,
                         (self.x, self.y, self.size, self.size))
        if self.symbol != '@':
            font = pygame.font.SysFont(None, 24)
            hp_text = font.render(f"{self.hp}", True, BLACK)
            tx = self.x + self.size/2 - hp_text.get_width()/2
            ty = self.y - 15
            pygame.display.get_surface().blit(hp_text, (tx, ty))

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
                    other.x += -ox * 0.1
                    other.y += -oy * 0.1
                    break

    def attack(self, player):
        now = time.time()
        if now - self.last_attack_time >= self.attack_speed:
            dist = math.hypot(player.x - self.x, player.y - self.y)
            if dist <= TILE_SIZE and now - player.last_damage_time >= 1:
                player.hp -= self.damage
                player.last_damage_time = now
            self.last_attack_time = now

    def attack_enemies(self, enemies, bosses=None):
        """
        플레이어가 적(enemies)과 보스(bosses)를 공격할 때 호출합니다.
        - 공격 속도(self.attack_speed) 쿨타임을 지켜서 발동
        - 공격 범위 = TILE_SIZE 이내에서 가장 먼저 만난 대상 하나에만 데미지
        - hp <= 0이 되면, 해당 원본 리스트에서 제거
        """
        now = time.time()
        if now - self.last_attack_time < self.attack_speed:
            return

        # 공격 대상 후보 합치기
        targets = []
        if enemies:
            targets.extend(enemies)
        if bosses:
            targets.extend(bosses)

        # 플레이어 중심 좌표
        cx = self.x + self.size / 2
        cy = self.y + self.size / 2

        for enemy in targets:
            ex = enemy.x + enemy.size / 2
            ey = enemy.y + enemy.size / 2
            dist = math.hypot(ex - cx, ey - cy)
            if dist <= TILE_SIZE:
                # 데미지 적용
                enemy.hp -= self.damage
                self.last_attack_time = now

                # 적 사망 시 실제 원본 리스트에서 제거
                if enemy.hp <= 0:
                    if enemies and enemy in enemies:
                        enemies.remove(enemy)
                    elif bosses and enemy in bosses:
                        bosses.remove(enemy)
                break
