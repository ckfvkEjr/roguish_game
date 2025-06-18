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

def generate_grid_map(n, start, boss, branch_chance=0.2):
    """
    n x n 그리드에 start, boss를 1로 설정 후,
    1) 메인 경로 생성(carve_main_path)
    2) 메인 경로 전체에 대해 분기 경로(add_branches)
       * 분기 경로는 다른 경로와 접촉하지 않도록
    """
    # 초기 0/1 그리드
    grid = [[0] * n for _ in range(n)]
    sx, sy = start
    bx, by = boss
    grid[sy][sx] = 1
    grid[by][bx] = 1

    # 1) 메인 경로 생성: 시작->보스
    def carve_main_path():
        cx, cy = sx, sy
        path = [(cx, cy)]
        while (cx, cy) != (bx, by):
            # 목표 방향 차이 계산
            dx, dy = bx - cx, by - cy
            moves = []
            if dx != 0:
                moves.append((cx + (1 if dx > 0 else -1), cy))
            if dy != 0:
                moves.append((cx, cy + (1 if dy > 0 else -1)))
            # 경로 선택에 약간 랜덤성 추가
            next_x, next_y = random.choice(moves)
            # 범위 내에서만 진행
            if 0 <= next_x < n and 0 <= next_y < n:
                cx, cy = next_x, next_y
                if grid[cy][cx] == 0:
                    grid[cy][cx] = 1
                    path.append((cx, cy))
        return path

    main_path = carve_main_path()

    # 2) 분기 경로 추가: main_path의 각 좌표에서
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    diag = [(1,1),(1,-1),(-1,1),(-1,-1)]

    def valid_branch(x, y, parent):
        # 범위 및 비어있는지
        if not (0 <= x < n and 0 <= y < n): return False
        if grid[y][x] != 0: return False
        # 인접성 확인
        px, py = parent
        if abs(x-px)+abs(y-py) != 1: return False
        # 주변 8방향에 다른 path가 있으면 안 됨 (parent 제외)
        for dx, dy in dirs+diag:
            nx, ny = x+dx, y+dy
            if (nx,ny) != parent and 0 <= nx < n and 0 <= ny < n:
                if grid[ny][nx] == 1:
                    return False
        return True

    for (px, py) in main_path:
        if random.random() < branch_chance:
            # 분기 길 길이
            length = random.randint(1,3)
            cx, cy = px, py
            for _ in range(length):
                random.shuffle(dirs)
                for dx, dy in dirs:
                    nx, ny = cx+dx, cy+dy
                    if valid_branch(nx, ny, (cx, cy)):
                        grid[ny][nx] = 1
                        cx, cy = nx, ny
                        break
    return grid


def generate_map_with_predefined_rooms(width, height):
    """
    Isaac 스타일 그리드 생성으로 맵 데이터와 연결 정보를 반환합니다.
    시작방은 중앙, 보스방은 테두리 좌표에서만 랜덤 선택
    """
    # 시작/보스 좌표 설정
    sx, sy = width//2, height//2
    borders = [(x,y) for x in range(width) for y in range(height)
               if (x==0 or x==width-1 or y==0 or y==height-1) and (x,y)!=(sx,sy)]
    bx, by = random.choice(borders)

    # 그리드 생성
    grid = generate_grid_map(width, (sx,sy), (bx,by))

    # 데이터 초기화
    map_data = {}
    room_connections = {}

    # 연결 정보 구성
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                conns = {"up":False, "down":False, "left":False, "right":False}
                if y>0 and grid[y-1][x]==1: conns["up"] = True
                if y<height-1 and grid[y+1][x]==1: conns["down"] = True
                if x>0 and grid[y][x-1]==1: conns["left"] = True
                if x<width-1 and grid[y][x+1]==1: conns["right"] = True
                room_connections[(x,y)] = conns

    # 방 레이아웃 배치
    from game.mapset import predefined_rooms, start_rooms, boss_room
    for (x,y), conns in room_connections.items():
        if (x,y)==(sx,sy):
            base = random.choice(list(start_rooms.values()))
        elif (x,y)==(bx,by):
            base = random.choice(list(boss_room.values()))
        else:
            base = random.choice(list(predefined_rooms.values()))
        room = [row.copy() for row in base]
        room = add_doors_to_room(room, conns)
        map_data[(x,y)] = room

    return map_data, room_connections, (sx,sy), (bx,by)


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

def generate_enemies_for_room(tilemap, room_x, room_y, start_x, start_y, diff):
    """
    1) 시작 방이면 빈 리스트 반환
    2) tilemap을 순회하면서 tile == 4인 칸만 '가능 위치'에 추가
    3) rate 확률로 스폰
    """
    # 시작 방이면 적 생성 안 함
    if (room_x, room_y) == (start_x, start_y):
        print(f"[generate_enemies] 시작 방 ({room_x},{room_y}) -> 생성 안 함")
        return []

    enemies = []
    possible_positions = []

    # 1) 빈 칸(tile==4) 세기
    for r in range(len(tilemap)):
        for c in range(len(tilemap[r])):
            if tilemap[r][c] == 4:
                possible_positions.append((c, r))

    print(f"[generate_enemies] 방 ({room_x},{room_y})에서 '4' 타일 개수:", len(possible_positions))

    # 2) 확률 계산
    rate = 0.1 + 0.05 * (diff - 1)
    print(f"[generate_enemies] 난이도 diff={diff}, 확률 rate={rate:.3f}")

    # 3) 실제 스폰 시도
    for (c, r) in possible_positions:
        if random.random() < rate:
            et = random.choice(list(config.enemy_types(diff).keys()))
            e = Entity(c * TILE_SIZE, r * TILE_SIZE, et, entity_type=et)
            enemies.append(e)
            print(f"  → 스폰: 타입 {et} 위치 ({c},{r})")

    print(f"[generate_enemies] 최종 생성된 적 개수:", len(enemies))
    return enemies

def generate_boss_for_room(tilemap, diff):
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
                      explored_rooms, start_x, start_y,
                      boss_x, boss_y):
    """
    direction: "up", "down", "left", "right"
    player: Entity
    current_x, current_y: 현재 방 좌표
    map_data: {(x,y) -> 9x9 타일맵}
    room_connections: {(x,y) -> {"up":bool, …}}
    explored_rooms: {(x,y) -> bool}
    start_x, start_y: 시작 방 좌표
    boss_x, boss_y: 보스 방 좌표

    반환값: (new_x, new_y, new_tilemap, new_enemies)
    """
    tilemap      = map_data[(current_x, current_y)]
    conns        = room_connections[(current_x, current_y)]

    # 1) 문 통과 여부 체크
    if not check_player_at_door(player, direction, tilemap, conns):
        return current_x, current_y, tilemap, []

    # 2) 연결 정보가 False면 이동 불가
    if not conns.get(direction):
        return current_x, current_y, tilemap, []

    # 3) 실제 좌표(방 번호) 변경 및 플레이어 재배치
    if direction == "up":
        new_x, new_y = current_x, current_y - 1
        player.x, player.y = TILE_SIZE * 4, TILE_SIZE * 8
    elif direction == "down":
        new_x, new_y = current_x, current_y + 1
        player.x, player.y = TILE_SIZE * 4, TILE_SIZE
    elif direction == "left":
        new_x, new_y = current_x - 1, current_y
        player.x, player.y = TILE_SIZE * 8, TILE_SIZE * 4
    else:  # "right"
        new_x, new_y = current_x + 1, current_y
        player.x, player.y = TILE_SIZE, TILE_SIZE * 4

    # 4) 새로운 방 불러오기
    new_tilemap = map_data[(new_x, new_y)]
    new_conns   = room_connections[(new_x, new_y)]
    new_tilemap = add_doors_to_room(new_tilemap, new_conns)

    # 5) 적/보스 생성 여부 판단
    if not explored_rooms.get((new_x, new_y), False):
        if (new_x, new_y) == (boss_x, boss_y):
            new_enemies = generate_boss_for_room(new_tilemap, config.itdiff())
        else:
            new_enemies = generate_enemies_for_room(
                tilemap=new_tilemap,
                room_x=new_x, room_y=new_y,
                start_x=start_x, start_y=start_y, diff=config.itdiff()
            )
    else:
        new_enemies = []  # 이미 방문한 방이면 적 제거

    # 6) 탐험 플래그 갱신
    explored_rooms[(new_x, new_y)] = True

    return new_x, new_y, new_tilemap, new_enemies