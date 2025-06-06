# game/entity.py

import pygame
import math
import time
from game.config import TILE_SIZE, RED, BLACK, diff, enemy_types, boss_types
from game.collision import check_corner_collision

class Entity:
    def __init__(self, x, y, symbol, entity_type="player"):
        self.x = x
        self.y = y
        self.symbol = symbol

        if entity_type == "player":
            self.hp               = 100
            self.speed            = (TILE_SIZE/50)*2 + (TILE_SIZE/50)*0.25*diff
            self.color            = RED
            self.attack_speed     = 0.75 - 0.025*diff
            self.damage           = 5
            self.size             = TILE_SIZE * 0.25
            self.last_damage_time = 0
            self.last_attack_time = 0
            self.last_direction   = "down"
        elif entity_type.startswith("B_"):
            attrs = boss_types(diff).get(entity_type, boss_types(diff)["B_a"])
            self.hp               = attrs["hp"]
            self.speed            = attrs["speed"]
            self.color            = attrs["color"]
            self.attack_speed     = attrs["attack_speed"]
            self.damage           = attrs["damage"]
            self.size             = attrs["size"]
            self.last_attack_time = 0
        else:
            attrs = enemy_types(diff).get(entity_type, enemy_types(diff)["a"])
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
        center = (int(self.x + self.size/2), int(self.y + self.size/2))
        pygame.draw.circle(pygame.display.get_surface(), (255, 255, 0),
                           center, TILE_SIZE*2, 1)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def move_towards(self, target_x, target_y, stop_distance=10, enemies=None):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > stop_distance:
            dx, dy = dx/dist, dy/dist
            self.x += dx * self.speed
            self.y += dy * self.speed

            if enemies:
                for other in enemies:
                    if other is not self and check_corner_collision(self, other):
                        ox = (self.get_rect().centerx - other.get_rect().centerx)/2
                        oy = (self.get_rect().centery - other.get_rect().centery)/2
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
