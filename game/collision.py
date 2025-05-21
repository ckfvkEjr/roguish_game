# game/collision.py

import pygame
from game.config import TILE_SIZE, walkable_tiles, door

def check_tile_collision(x, y, size, tilemap):
    """타일맵 경계 및 벽(walkable_tiles 외)에 부딪히는지 확인합니다."""
    corners = [(x, y), (x+size-1, y), (x, y+size-1), (x+size-1, y+size-1)]
    for cx, cy in corners:
        tx = int(cx // TILE_SIZE)
        ty = int(cy // TILE_SIZE)
        if tx < 0 or ty < 0 or ty >= len(tilemap) or tx >= len(tilemap[0]):
            return True
        if tilemap[ty][tx] not in walkable_tiles:
            return True
    return False

def check_corner_collision(entity1, entity2):
    """두 엔티티의 네 모서리 점 간 충돌 검사."""
    corners = [
        (entity1.x, entity1.y),
        (entity1.x+entity1.size-1, entity1.y),
        (entity1.x, entity1.y+entity1.size-1),
        (entity1.x+entity1.size-1, entity1.y+entity1.size-1)
    ]
    for cx, cy in corners:
        if entity2.get_rect().collidepoint(cx, cy):
            return True
    return False

def check_player_enemy_collision(player, enemies, tilemap):
    """플레이어와 적이 충돌 시 서로 살짝 밀쳐냅니다."""
    for enemy in enemies:
        if check_corner_collision(player, enemy):
            ox = (enemy.get_rect().centerx - player.get_rect().centerx) / 2
            oy = (enemy.get_rect().centery - player.get_rect().centery) / 2
            if not check_tile_collision(enemy.x+ox, enemy.y, enemy.size, tilemap):
                enemy.x += ox * 0.1
            if not check_tile_collision(enemy.x, enemy.y+oy, enemy.size, tilemap):
                enemy.y += oy * 0.1
            return True
    return False

def check_player_at_door(player, direction, tilemap, room_conns):
    """플레이어가 방 경계의 문 위치에 있는지 확인합니다."""
    if direction == "up" and player.y <= 0 and room_conns.get("up") and tilemap[0][4] == door:
        return True
    if direction == "down" and player.y >= TILE_SIZE*8 and room_conns.get("down") and tilemap[8][4] == door:
        return True
    if direction == "left" and player.x <= 0 and room_conns.get("left") and tilemap[4][0] == door:
        return True
    if direction == "right" and player.x >= TILE_SIZE*8 and room_conns.get("right") and tilemap[4][8] == door:
        return True
    return False
