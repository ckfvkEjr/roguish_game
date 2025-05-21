# game/map_tools.py

import random
from collections import deque
import pygame
import math
import time
from game.config import TILE_SIZE, walkable_tiles, door, diff, BLUE, BLACK, VIOLET, WHITE, GREEN
import game.config as config
from game.mapset import predefined_rooms, start_rooms, boss_room
from game.entity import Entity

def generate_room_connections_with_constraints(width, height, branch_probability=0, max_connections=3):
    """
    DFS 기반으로 기본 미로를 생성하면서 분기점(branch)과 교차로를 제한적으로 추가합니다.
    Returns:
        connections: dict[(x,y)] -> {"up":bool, "down":bool, "left":bool, "right":bool}
    """
    connections = {(x, y): {"up": False, "down": False, "left": False, "right": False}
                   for x in range(width) for y in range(height)}
    visited = {(x, y): False for x in range(width) for y in range(height)}
    stack = []
    start_x, start_y = width // 2, height // 2
    stack.append((start_x, start_y))
    visited[(start_x, start_y)] = True
    directions = [("up", 0, -1), ("down", 0, 1), ("left", -1, 0), ("right", 1, 0)]
    reverse = {"up": "down", "down": "up", "left": "right", "right": "left"}
    while stack:
        cx, cy = stack[-1]
        random.shuffle(directions)
        found = False
        for dir_name, dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[(nx, ny)]:
                if sum(connections[(cx, cy)].values()) < max_connections:
                    connections[(cx, cy)][dir_name] = True
                    connections[(nx, ny)][reverse[dir_name]] = True
                    visited[(nx, ny)] = True
                    stack.append((nx, ny))
                    found = True
                    break
        if not found:
            stack.pop()
        if random.random() < branch_probability:
            for dir_name, dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if (0 <= nx < width and 0 <= ny < height and visited[(nx, ny)]
                        and sum(connections[(cx, cy)].values()) < max_connections):
                    connections[(cx, cy)][dir_name] = True
                    connections[(nx, ny)][reverse[dir_name]] = True
    return connections

def add_doors_to_room(room, connections):
    """
    방 중앙 벽에 문(door)을 추가한 뒤, 실제 연결 여부에 따라
    연결이 없는 쪽은 벽(1)으로 되돌립니다.
    """
    room[0][4] = door
    room[8][4] = door
    room[4][0] = door
    room[4][8] = door
    if not connections.get("up"):
        room[0][4] = 1
    if not connections.get("down"):
        room[8][4] = 1
    if not connections.get("left"):
        room[4][0] = 1
    if not connections.get("right"):
        room[4][8] = 1
    return room

def select_boss_room_with_constraints(connections, start_x, start_y, width, height):
    """
    시작 방에서 BFS로 거리를 계산한 뒤,
    연결 수가 1개인 방들 중 랜덤하게 가장 먼 방을 보스룸으로 선택합니다.
    """
    queue = deque([(start_x, start_y)])
    visited = {(x, y): False for x in range(width) for y in range(height)}
    distances = {(x, y): 0 for x in range(width) for y in range(height)}
    visited[(start_x, start_y)] = True
    while queue:
        cx, cy = queue.popleft()
        for dir_name, (dx, dy) in {"up": (0,-1), "down": (0,1), "left": (-1,0), "right": (1,0)}.items():
            if connections[(cx, cy)].get(dir_name):
                nx, ny = cx + dx, cy + dy
                if not visited[(nx, ny)]:
                    visited[(nx, ny)] = True
                    distances[(nx, ny)] = distances[(cx, cy)] + 1
                    queue.append((nx, ny))
    candidates = [(x, y) for (x, y), conn in connections.items() if sum(conn.values()) == 1]
    if candidates:
        max_dist = max(distances[pos] for pos in candidates)
        farthest = [pos for pos in candidates if distances[pos] == max_dist]
        return random.choice(farthest)
    return (width - 1, height - 1)

def generate_map_with_predefined_rooms(width, height):
    """
    미리 정의된 방 세트(predefined_rooms, start_rooms, boss_room)를
    랜덤하게 배치하여 전체 맵을 생성합니다.
    Returns:
        map_data, room_connections, (start_x, start_y), (boss_x, boss_y)
    """
    room_connections = generate_room_connections_with_constraints(
        width, height,
        branch_probability=0.1 + config.itdiff() * 0.05,
        max_connections=3
    )
    map_data = {}
    start_x, start_y = width // 2, height // 2
    boss_x, boss_y = select_boss_room_with_constraints(
        room_connections, start_x, start_y, width, height
    )
    for y in range(height):
        for x in range(width):
            layout = random.choice(list(predefined_rooms.values()))
            room_matrix = [row.copy() for row in layout]
            map_data[(x, y)] = add_doors_to_room(
                room_matrix, room_connections[(x, y)]
            )
    start_layout = random.choice(list(start_rooms.values()))
    map_data[(start_x, start_y)] = add_doors_to_room(
        [row.copy() for row in start_layout],
        room_connections[(start_x, start_y)]
    )
    boss_layout = random.choice(list(boss_room.values()))
    map_data[(boss_x, boss_y)] = add_doors_to_room(
        [row.copy() for row in boss_layout],
        room_connections[(boss_x, boss_y)]
    )
    return map_data, room_connections, (start_x, start_y), (boss_x, boss_y)

def check_player_at_door(player, direction, tilemap, room_conns):
    """
    플레이어가 방 경계의 문 위치에 있는지 확인합니다.
    """
    if direction == "up" and player.y <= 0 and room_conns.get("up") and tilemap[0][4] == door:
        return True
    if direction == "down" and player.y >= TILE_SIZE*8 and room_conns.get("down") and tilemap[8][4] == door:
        return True
    if direction == "left" and player.x <= 0 and room_conns.get("left") and tilemap[4][0] == door:
        return True
    if direction == "right" and player.x >= TILE_SIZE*8 and room_conns.get("right") and tilemap[4][8] == door:
        return True
    return False

from game.collision import check_tile_collision, check_corner_collision, check_player_enemy_collision, check_player_at_door

def generate_enemies_for_room(tilemap, room_x, room_y, start_x, start_y):
    """
    현재 방의 타일맵을 기반으로 적을 생성합니다.
    시작 방(start_x, start_y)에서는 적을 생성하지 않습니다.
    Returns:
        list of Entity
    """
    if (room_x, room_y) == (start_x, start_y):
        return []
    enemies = []
    rate = 0.1 + 0.05 * (diff - 1)
    for row in range(len(tilemap)):
        for col in range(len(tilemap[row])):
            if tilemap[row][col] == 4 and random.random() < rate:
                et = random.choice(list(config.enemy_types(diff).keys()))
                e = Entity(col*TILE_SIZE, row*TILE_SIZE, et, entity_type=et)
                enemies.append(e)
    return enemies

def generate_boss_for_room(tilemap):
    """
    현재 보스룸의 타일맵을 기반으로 보스를 생성합니다.
    Returns:
        list with one boss Entity
    """
    bosses = []
    for row in range(len(tilemap)):
        for col in range(len(tilemap[row])):
            if tilemap[row][col] == 5:
                bt = random.choice(list(config.boss_types(diff).keys()))
                b = Entity(col*TILE_SIZE, row*TILE_SIZE, bt, entity_type=bt)
                bosses.append(b)
                return bosses
    return bosses

def draw_tilemap(tilemap):
    """
    타일맵(9x9) 을 화면에 그립니다.
    """
    screen = pygame.display.get_surface()
    for r, row in enumerate(tilemap):
        for c, tile in enumerate(row):
            x, y = c*TILE_SIZE, r*TILE_SIZE
            if tile == 1:
                color = BLUE
            elif tile == 2:
                color = BLACK
            elif tile == door:
                color = VIOLET
            else:
                color = WHITE
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))

def move_to_next_room(direction, player,
                      current_x, current_y,
                      map_data, room_connections,
                      explored_rooms,
                      start_x, start_y,
                      boss_x, boss_y):
    """
    주어진 방향으로 문을 통해 다음 방으로 이동하고
    플레이어 위치, current_x/y, tilemap, enemies 를 반환합니다.
    """
    tilemap = map_data[(current_x, current_y)]
    conns = room_connections[(current_x, current_y)]
    # 문 통과 가능 여부 확인
    if not check_player_at_door(player, direction, tilemap, conns):
        return current_x, current_y, tilemap, []
    if not conns.get(direction):
        return current_x, current_y, tilemap, []
    # 좌표 변경 및 플레이어 초기 위치 설정
    if direction == "up":
        nx, ny = current_x, current_y - 1
        player.x, player.y = TILE_SIZE*4, TILE_SIZE*8
    elif direction == "down":
        nx, ny = current_x, current_y + 1
        player.x, player.y = TILE_SIZE*4, TILE_SIZE
    elif direction == "left":
        nx, ny = current_x - 1, current_y
        player.x, player.y = TILE_SIZE*8, TILE_SIZE*4
    else:  # right
        nx, ny = current_x + 1, current_y
        player.x, player.y = TILE_SIZE, TILE_SIZE*4
    # 새로운 방 정보
    new_tilemap = map_data[(nx, ny)]
    # 적/보스 생성
    if not explored_rooms.get((nx, ny), False):
        if (nx, ny) == (boss_x, boss_y):
            enemies = generate_boss_for_room(new_tilemap)
        else:
            enemies = generate_enemies_for_room(new_tilemap, nx, ny, start_x, start_y)
    else:
        enemies = []
    explored_rooms[(nx, ny)] = True
    return nx, ny, new_tilemap, enemies