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

def main():
    # 초기화
    pygame.init()
    pygame.display.set_caption('로그라이크 맵')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # 맵 생성
    map_data, room_connections, (start_x, start_y), (boss_x, boss_y) =         generate_map_with_predefined_rooms(MAP_WIDTH, MAP_HEIGHT)
    debug.print_map_data(map_data, MAP_WIDTH, MAP_HEIGHT)
    debug.print_room_connections(room_connections, MAP_WIDTH, MAP_HEIGHT)

    # 플레이어 및 적/보스 초기 설정
    player = Entity(TILE_SIZE*4.5, TILE_SIZE*4.5, '@', entity_type="player")
    current_x, current_y = start_x, start_y
    tilemap = map_data[(current_x, current_y)]
    enemies = generate_enemies_for_room(tilemap, current_x, current_y, start_x, start_y)
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

        # 방 이동: 방 안에 적이 없을 때만 이동 허용
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
                    tilemap = new_tilemap
                    enemies = new_enemies
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
                    tilemap = new_tilemap
                    enemies = new_enemies
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
                    tilemap = new_tilemap
                    enemies = new_enemies
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
                    tilemap = new_tilemap
                    enemies = new_enemies

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
        if not check_tile_collision(new_x, player.y, player.size, tilemap) and            not check_player_enemy_collision(player, enemies, tilemap):
            player.x = new_x
        if not check_tile_collision(player.x, new_y, player.size, tilemap) and            not check_player_enemy_collision(player, enemies, tilemap):
            player.y = new_y

        # 공격 처리
        if keys[pygame.K_SPACE]:
            player.attack_time = time.time()
            # 엔티티 공격 로직 필요 시 추가

        # 적 행동
        for enemy in enemies:
            enemy.move_towards(player.x, player.y, enemies=enemies)
            enemy.attack(player)
            enemy.draw()

        # 보스 행동
        for b in boss:
            b.move_towards(player.x, player.y, enemies=enemies)
            b.attack(player)
            b.draw()

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

        # 미니맵 등 UI 요소를 마지막에 그린다
        minimap.draw_minimap(explored_rooms, current_x, current_y,
                             MAP_WIDTH, MAP_HEIGHT, len(enemies), room_connections)

        # 화면 업데이트
        pygame.display.flip()
        # ───────────────────────────────────

        clock.tick(60)

if __name__ == '__main__':
    main()
