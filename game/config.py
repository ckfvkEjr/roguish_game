import pygame

# 화면 크기
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# 색상
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
BLUE   = (  0,   0, 255)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
YELLOW = (255, 255,   0)  # 공격 범위 색상
VIOLET = (238, 130, 238)

# 타일 크기
TILE_SIZE = 75

# 불·가능 타일 정의
door               = 3
walkable_tiles     = {0,3,4,5}
non_walkable_tiles = {1,2}

# 화면(surface)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 난이도(diff) 관리
diff = 1
def diffs(x):
    global diff
    diff += x
def reset_diff():
    global diff
    diff = 1
def itdiff():
    return int(diff)

# 맵 크기
def map_size(diff):
    MAP_WIDTH  = 1 + 2 * diff
    MAP_HEIGHT = 1 + 2 * diff

# 점수 처리
scores = 0
def score(x):
    global scores
    scores += x
def reset_score():
    global scores
    scores = 0
def getscore():
    return scores

# (원본에 있던) 적·보스 속성 함수
def enemy_types(diff):
    return {
        "a": {"hp":5+(diff-1)*2, "speed":(TILE_SIZE/50)*0.1+diff*(TILE_SIZE/50)*0.01, "color":RED, "attack_speed":1+diff*0.05, "damage":2+(diff-1), "size":TILE_SIZE*0.25},
        "b": {"hp":8+(diff-1)*2, "speed":(TILE_SIZE/50)*0.1+diff*(TILE_SIZE/50)*0.01, "color":GREEN, "attack_speed":1.5+diff*0.05, "damage":3+(diff-1), "size":TILE_SIZE*0.3},
        "c": {"hp":10+(diff-1)*2,"speed":(TILE_SIZE/50)*0.08+diff*(TILE_SIZE/50)*0.01,"color":BLUE,"attack_speed":2+diff*0.05,"damage":4+(diff-1),"size":TILE_SIZE*0.35},
    }

def boss_types(diff):
    return {
        "B_a": {"hp":25+(diff-1)*2,"speed":(TILE_SIZE/50)*0.21+diff*(TILE_SIZE/50)*0.01,"color":VIOLET,"attack_speed":1+diff*0.05,"damage":2+(diff-1)*2,"size":TILE_SIZE*0.5},
        "B_b": {"hp":50+(diff-1)*2,"speed":(TILE_SIZE/50)*0.18+diff*(TILE_SIZE/50)*0.01,"color":VIOLET,"attack_speed":1.5+diff*0.05,"damage":3+(diff-1)*2,"size":TILE_SIZE*0.6},
        "B_c": {"hp":75+(diff-1)*2,"speed":(TILE_SIZE/50)*0.12+diff*(TILE_SIZE/50)*0.01,"color":VIOLET,"attack_speed":2+diff*0.05,"damage":4+(diff-1)*2,"size":TILE_SIZE*0.7},
    }
