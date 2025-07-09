# game/minimap.py

import pygame
from game.config import *
import game.config as config

def draw_minimap(explored_rooms, current_x, current_y, width, height, texts, room_connections):
    global diff
    minimap_size = (TILE_SIZE/50)*125
    minimap_x = SCREEN_WIDTH - minimap_size - 10
    minimap_y = SCREEN_HEIGHT - minimap_size - 10
    font = pygame.font.SysFont(None, 24)
    
    screen = pygame.display.get_surface()
    pygame.draw.rect(screen, BLACK, (minimap_x, minimap_y - 85, 200, 90))
    
    text = f"enemies : {texts}"
    text2 = f"x : {current_x}, y : {current_y}"
    text3 = f"stage : {config.itdiff()}"
    ts   = font.render(text,  True, WHITE)
    ts2  = font.render(text2, True, WHITE)
    ts3 = font.render(text3, True, WHITE)

    screen.blit(ts3,  (minimap_x, minimap_y - 80))
    screen.blit(ts,  (minimap_x, minimap_y - 60))
    screen.blit(ts2, (minimap_x, minimap_y - 40))
    
    room_w = minimap_size / width
    room_h = minimap_size / height

    # 배경
    pygame.draw.rect(screen, BLACK, (minimap_x, minimap_y, minimap_size, minimap_size))

    # 탐험된 방
    for (x,y), seen in explored_rooms.items():
        if seen:
            pygame.draw.rect(screen, WHITE,
                             (minimap_x + x*room_w,
                              minimap_y + y*room_h,
                              room_w, room_h))

    # 현재 방 강조
    pygame.draw.rect(screen, RED,
                     (minimap_x + current_x*room_w,
                      minimap_y + current_y*room_h,
                      room_w, room_h), 2)

    # 연결선
    for y in range(height):
        for x in range(width):
            if not explored_rooms.get((x,y), False):
                continue
            cx = minimap_x + (x+0.5)*room_w
            cy = minimap_y + (y+0.5)*room_h
            conn = room_connections.get((x,y), {})
            if conn.get("up")   and explored_rooms.get((x, y-1), False):
                pygame.draw.line(screen, GREEN, (cx, cy),
                                 (cx, minimap_y+(y-1+0.5)*room_h), 2)
            if conn.get("down") and explored_rooms.get((x, y+1), False):
                pygame.draw.line(screen, GREEN, (cx, cy),
                                 (cx, minimap_y+(y+1+0.5)*room_h), 2)
            if conn.get("left") and explored_rooms.get((x-1, y), False):
                pygame.draw.line(screen, GREEN, (cx, cy),
                                 (minimap_x+(x-1+0.5)*room_w, cy), 2)
            if conn.get("right")and explored_rooms.get((x+1, y), False):
                pygame.draw.line(screen, GREEN, (cx, cy),
                                 (minimap_x+(x+1+0.5)*room_w, cy), 2)
