import pygame
import sys
from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
import game.config as config
import game.debug as debug
import game.minimap as minimap
from game.map_tools import (
    generate_map_with_predefined_rooms,
    draw_tilemap,
    move_to_next_room,
    generate_enemies_for_room,
    generate_boss_for_room
)
from game.entity import Entity
from game.collision import check_tile_collision, check_player_enemy_collision

    # ─── 전역 상태 관리 변수 ───
stage = 1           # 현재 스테이지 (1부터 시작)
boss_active = False # 보스 방 입장 후 처치 대기 중인지 여부

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
        if len(enemies) == 0:
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

        # 충돌 검사
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
        # boss_active가 True 이면서 boss 리스트가 비어 있으면
        if boss_active and len(boss) == 0:
            # 1) 보스 처치 단계 종료
            boss_active = False
            # 2) 스테이지 번호 1 증가
            stage += 1
            # 3) diff(난이도) 수치 1 증가
            config.diffs(1)      # 또는 diff += 1 해도 되지만, config 내부 함수를 권장
            # 4) 새로운 맵 생성 (diff가 바뀌면서 MAP_WIDTH/HEIGHT도 변경됨)
            diff = config.itdiff()
            MAP_HEIGHT = MAP_HEIGHT + 2
            MAP_WIDTH = MAP_WIDTH + 2
            map_data, room_connections, (start_x, start_y), (boss_x, boss_y) = \
                generate_map_with_predefined_rooms(MAP_WIDTH, MAP_HEIGHT)
            debug.print_map_data(map_data, MAP_WIDTH, MAP_HEIGHT)
            debug.print_room_connections(room_connections, MAP_WIDTH, MAP_HEIGHT)

            # 5) 플레이어·적·보스 초기화
            current_x, current_y = start_x, start_y
            tilemap = map_data[(current_x, current_y)]
            player.x, player.y = TILE_SIZE*4, TILE_SIZE*4 
            
            enemies = generate_enemies_for_room(tilemap, current_x, current_y, start_x, start_y, config.itdiff())
            boss    = []  # 보스는 빈 리스트로 시작 (다음 보스 방 입장 시 생성)

            # 6) 탐험 기록(미니맵) 초기화
            explored_rooms = { (x, y): False for x in range(MAP_WIDTH) for y in range(MAP_HEIGHT) }
            explored_rooms[(current_x, current_y)] = True

        # 탐험 상태 업데이트
        explored_rooms[(current_x, current_y)] = True

        screen.fill(BLACK)

        # 맵(타일)을 먼저 그린다
        draw_tilemap(tilemap)

        # 적·보스 그리기 (적이 맵 위에 올려지도록)
        for enemy in enemies:
            enemy.draw()
        for b in boss:
            b.draw()

        # 플레이어를 그린다 (플레이어가 적보다 위에 보이길 원하면 이 위치를 바꿔도 됩니다)
        player.draw()   

        #공격 범위(디버그용)
        player.draw_attack_range()
        # 미니맵 등 UI 요소를 마지막에 그린다
        minimap.draw_minimap(explored_rooms, current_x, current_y,
                             MAP_WIDTH, MAP_HEIGHT, len(enemies), room_connections)

        # 화면 업데이트
        pygame.display.flip()
        # ───────────────────────────────────
        
        clock.tick(60)

if __name__ == '__main__':
    main()
