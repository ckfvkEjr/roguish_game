import pygame
import sys
import time
from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
import game.config as config
import game.debug as debug
import game.minimap as minimap
from game.map_tools import (
    generate_map_with_predefined_rooms,
    draw_tilemap,
    move_to_next_room,
    generate_enemies_for_room,
    generate_boss_for_room,
    generate_items_for_room
)
from game.entity import Entity
from game.collision import check_tile_collision, check_player_enemy_collision
from game.itemset import item_types

    # ─── 전역 상태 관리 변수 ───
stage = 1           # 현재 스테이지 (1부터 시작)
boss_active = False # 보스 방 입장 후 처치 대기 중인지 여부
next_stage_active = False        # 추가: 다음 스테이지 타일 활성화 플래그
next_stage_timer = None         # 추가: 타이머 시작 시간
game_over = False
items = []
room_items = {}

def apply_item_effect(player, item_data):
    if item_data.get("hp") is not None:
        player.hp = min(player.hp + item_data["hp"], player.max_hp)
    if item_data.get("max_hp") is not None:
        player.max_hp += item_data["max_hp"]
        player.hp = min(player.hp, player.max_hp)
    if item_data.get("speed") is not None:
        player.speed += item_data["speed"]
    if item_data.get("attack_speed") is not None:
        player.attack_speed += item_data["attack_speed"]
    if item_data.get("damage") is not None:
        player.damage += item_data["damage"]
    if item_data.get("size") is not None:
        player.size += item_data["size"]

def check_collision(player, item):
    item_x = item.x + TILE_SIZE * 0.5 - item.size * 0.5
    item_y = item.y + TILE_SIZE * 0.5 - item.size * 0.5

    return (
        player.x < item_x + item.size and
        player.x + player.size > item_x and
        player.y < item_y + item.size and
        player.y + player.size > item_y
    )

def main():
    global boss_active, stage, MAP_WIDTH, MAP_HEIGHT
    # 초기화
    pygame.init()
    pygame.display.set_caption('로그라이크 맵')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # 맵 생성
    map_data, room_connections, (start_x, start_y), (boss_x, boss_y) = generate_map_with_predefined_rooms(MAP_WIDTH, MAP_HEIGHT)
    debug.print_map_data(map_data, MAP_WIDTH, MAP_HEIGHT)
    debug.print_room_connections(room_connections, MAP_WIDTH, MAP_HEIGHT)

    # 플레이어 및 적/보스 초기 설정
    player = Entity(TILE_SIZE*4.5, TILE_SIZE*4.5, '@', entity_type="player")
    current_x, current_y = start_x, start_y
    tilemap = map_data[(current_x, current_y)]
    enemies = generate_enemies_for_room(tilemap, current_x, current_y, start_x, start_y, config.itdiff())
    boss = []
    explored_rooms = {(x, y): False for x in range(MAP_WIDTH) for y in range(MAP_HEIGHT)}
    explored_rooms[(start_x, start_y)] = True

    # 메인 루프
    while True:
        global next_stage_active
        global game_over
        global items
        global room_items
        screen.fill(BLACK)
        # 이벤트 처리
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # 키 상태
        keys = pygame.key.get_pressed()

        # 방 이동 처리 (적이 모두 사라졌을 때만)
        if len(enemies) == 0 and len(boss) == 0:
            if keys[pygame.K_UP]:
                nx, ny, new_tilemap, new_enemies = move_to_next_room(
                    "up", player,
                    current_x, current_y,
                    map_data, room_connections,
                    explored_rooms,
                    start_x, start_y,
                    boss_x, boss_y
                )
                if (nx, ny) != (current_x, current_y):
                    current_x, current_y = nx, ny
                    tilemap  = new_tilemap
                    enemies  = new_enemies
                    if (nx, ny) not in room_items:
                        room_items[(nx, ny)] = generate_items_for_room(tilemap)
                        items = room_items[(nx, ny)]
                    # ─── 보스 방 입장 시 보스 생성 + boss_active 활성화 ───
                    if (current_x, current_y) == (boss_x, boss_y) and not boss_active:
                        print('보스 생성!')
                        boss = generate_boss_for_room(tilemap, config.itdiff())
                        boss_active = True
                        enemies = []

            elif keys[pygame.K_DOWN]:
                nx, ny, new_tilemap, new_enemies = move_to_next_room(
                    "down", player,
                    current_x, current_y,
                    map_data, room_connections,
                    explored_rooms,
                    start_x, start_y,
                    boss_x, boss_y
                )
                if (nx, ny) != (current_x, current_y):
                    current_x, current_y = nx, ny
                    tilemap  = new_tilemap
                    enemies  = new_enemies
                    if (nx, ny) not in room_items:
                        room_items[(nx, ny)] = generate_items_for_room(tilemap)
                        items = room_items[(nx, ny)]
                    if (current_x, current_y) == (boss_x, boss_y) and not boss_active:
                        boss = generate_boss_for_room(tilemap, config.itdiff())
                        boss_active = True
                        enemies = []

            elif keys[pygame.K_LEFT]:
                nx, ny, new_tilemap, new_enemies = move_to_next_room(
                    "left", player,
                    current_x, current_y,
                    map_data, room_connections,
                    explored_rooms,
                    start_x, start_y,
                    boss_x, boss_y
                )
                if (nx, ny) != (current_x, current_y):
                    current_x, current_y = nx, ny
                    tilemap  = new_tilemap
                    enemies  = new_enemies
                    if (nx, ny) not in room_items:
                        room_items[(nx, ny)] = generate_items_for_room(tilemap)
                        items = room_items[(nx, ny)]
                    if (current_x, current_y) == (boss_x, boss_y) and not boss_active:
                        print('보스 생성!')
                        boss = generate_boss_for_room(tilemap, config.itdiff())
                        boss_active = True
                        enemies = []

            elif keys[pygame.K_RIGHT]:
                nx, ny, new_tilemap, new_enemies = move_to_next_room(
                    "right", player,
                    current_x, current_y,
                    map_data, room_connections,
                    explored_rooms,
                    start_x, start_y,
                    boss_x, boss_y
                )
                if (nx, ny) != (current_x, current_y):
                    current_x, current_y = nx, ny
                    tilemap  = new_tilemap
                    enemies  = new_enemies
                    if (nx, ny) not in room_items:
                        room_items[(nx, ny)] = generate_items_for_room(tilemap)
                        items = room_items[(nx, ny)]
                    if (current_x, current_y) == (boss_x, boss_y) and not boss_active:
                        boss = generate_boss_for_room(tilemap, config.itdiff())
                        boss_active = True
                        enemies = []

        # 플레이어 이동
        new_x, new_y = player.x, player.y
        if keys[pygame.K_LEFT]:
            new_x -= player.speed
        if keys[pygame.K_RIGHT]:
            new_x += player.speed
        if keys[pygame.K_UP]:
            new_y -= player.speed
        if keys[pygame.K_DOWN]:
            new_y += player.speed

        # 충돌 검사 + 적 충돌 시스템 더해야 함 적,벽 / 
        if not check_tile_collision(new_x, player.y, player.size, tilemap) and            not check_player_enemy_collision(player, enemies + boss, tilemap):
            player.x = new_x
        if not check_tile_collision(player.x, new_y, player.size, tilemap) and            not check_player_enemy_collision(player, enemies + boss, tilemap):
            player.y = new_y

        # 공격 처리
        if keys[pygame.K_SPACE]:
            player.attack_enemies(enemies, boss)
        
        # 적 행동
        for enemy in enemies:
            enemy.move_towards(player.x, player.y, tilemap, enemies=enemies)
            check_player_enemy_collision(player, [enemy], tilemap) 
            enemy.attack(player)
            enemy.draw()

        # 보스 행동
        for b in boss:
            b.move_towards(player.x, player.y, tilemap, enemies=enemies)
            check_player_enemy_collision(player, [b], tilemap)
            b.attack(player)
            b.draw()
        
         # ─── 보스 처치 완료 판정 ───
        if boss_active and len(boss) == 0 and not next_stage_active:
            print("보스 리스트 길이:", len(boss))
            print("boss_active:", boss_active, "next_stage_active:", next_stage_active)
            boss_active = False
            next_stage_active = True
            # 보스방 중앙에 다음 스테이지 타일 설치
            center = len(tilemap) // 2
            tilemap[center][center] = config.next_stage  # config.next_stage 값(6)
            next_stage_timer = None
            # 탐험 상태 업데이트
            explored_rooms[(current_x, current_y)] = True

            screen.fill(BLACK)
        
        if next_stage_active == True:
            # 플레이어 중심 좌표로 타일 위치 계산
            px = int((player.x + player.size/2) // TILE_SIZE)
            py = int((player.y + player.size/2) // TILE_SIZE)
            if 0 <= px < len(tilemap[0]) and 0 <= py < len(tilemap):
                if tilemap[py][px] == config.next_stage:
                    if next_stage_timer is None:
                        next_stage_timer = time.time()
                    elif time.time() - next_stage_timer >= 2:
                        # 2초 이상 머물렀으면 스테이지 전환
                        stage += 1
                        config.diffs(1)
                        # 맵 크기 증가
                        MAP_HEIGHT = MAP_HEIGHT + 2
                        MAP_WIDTH = MAP_WIDTH + 2
                        # 새로운 맵 생성
                        map_data, room_connections, (start_x, start_y), (boss_x, boss_y) = \
                            generate_map_with_predefined_rooms(MAP_WIDTH, MAP_HEIGHT)
                        debug.print_map_data(map_data, MAP_WIDTH, MAP_HEIGHT)
                        debug.print_room_connections(room_connections, MAP_WIDTH, MAP_HEIGHT)
                        # 플레이어/적/보스 초기화 (원래 보스 kill 이후 로직)
                        current_x, current_y = start_x, start_y
                        tilemap = map_data[(current_x, current_y)]
                        player.x, player.y = TILE_SIZE*4, TILE_SIZE*4
                        enemies = generate_enemies_for_room(tilemap, current_x, current_y, start_x, start_y, config.itdiff())
                        boss = []
                        explored_rooms = { (x, y): False for x in range(MAP_WIDTH) for y in range(MAP_HEIGHT) }
                        explored_rooms[(current_x, current_y)] = True
                        next_stage_active = False
                        next_stage_timer = None

                else:
                    # 타일에서 벗어나면 타이머 리셋
                    next_stage_timer = None
        if (current_x, current_y) == (start_x, start_y) and tilemap[4][4] != 0:
            tilemap[4][4] = 0
            print("시작방!")

        if player.hp <= 0:
            game_over = True

        # 맵(타일)을 먼저 그린다
        draw_tilemap(tilemap)

        # 적·보스 그리기 (적이 맵 위에 올려지도록)
        for enemy in enemies:
            enemy.draw()
        for b in boss:
            b.draw()

        # 플레이어를 그린다 (플레이어가 적보다 위에 보이길 원하면 이 위치를 바꿔도 됩니다)
        player.draw()

        current_items = room_items.get((current_x, current_y), [])
        for item in current_items[:]:  # 복사본 반복
            if check_collision(player, item):
                from game.itemset import item_types
                item_data = item_types.get(item.symbol, {})
                apply_item_effect(player, item_data)
                current_items.remove(item)
                break  # 1개만 처리   
        
        for item in room_items.get((current_x, current_y), []):
            item.draw()

        if game_over:
            screen.fill(BLACK)
            # 게임 오버 텍스트 출력
            font = pygame.font.SysFont(None, 48)
            msg = font.render("GAME OVER - Press R to Restart", True, (255, 255, 255))
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2))
            player.hp = 0
            enemies = []
            boss = []
            # R 키 입력 시 초기화
            if keys[pygame.K_r]:
                stage = 1
                config.reset_diff()
                MAP_WIDTH = 9
                MAP_HEIGHT = 9
                map_data, room_connections, (start_x, start_y), (boss_x, boss_y) = generate_map_with_predefined_rooms(MAP_WIDTH, MAP_HEIGHT)
                current_x, current_y = start_x, start_y
                tilemap = map_data[(current_x, current_y)]
                player = Entity(TILE_SIZE*4.5, TILE_SIZE*4.5, '@', entity_type="player")
                enemies = generate_enemies_for_room(tilemap, current_x, current_y, start_x, start_y, config.itdiff())
                boss = []
                explored_rooms = {(x, y): False for x in range(MAP_WIDTH) for y in range(MAP_HEIGHT)}
                explored_rooms[(start_x, start_y)] = True
                game_over = False
                next_stage_active = False
                next_stage_timer = None

        # 미니맵 등 UI 요소를 마지막에 그린다
        minimap.draw_minimap(explored_rooms, current_x, current_y,
                             MAP_WIDTH, MAP_HEIGHT, len(enemies), room_connections)
        
                # ─── 플레이어 체력 UI 출력 ───
        font = pygame.font.SysFont(None, 24)
        hp_text = font.render(f"HP: {player.hp} / {player.max_hp}", True, (255, 255, 255))
        # 체력바 위치 및 크기
        bar_x = SCREEN_WIDTH - 240
        bar_y = 50
        bar_width = 200
        bar_height = 20
        hp_ratio = max(0, player.hp / player.max_hp)
        
        pygame.draw.rect(screen, BLACK, (bar_x - 10, bar_y - 30, bar_width + 20, bar_height + 40))

        # 체력바 배경 + 전경
        pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))       # 배경
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width * hp_ratio, bar_height))  # 빨간 체력바

        # 수치 텍스트
        screen.blit(hp_text, (bar_x + 60, bar_y - 25))


        # 화면 업데이트
        pygame.display.flip()
        # ───────────────────────────────────
        
        clock.tick(60)

if __name__ == '__main__':
    main()
