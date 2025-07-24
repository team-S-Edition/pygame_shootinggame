import pygame

# 味方の当たり判定
def hit_myplane(myplane_x, myplane_y):
    hit_myplane = pygame.Rect(myplane_x, myplane_y, 64, 64)
    return hit_myplane

# 敵の当たり判定
def hit_enemy(enemy01_x,enemy01_y):
    hit_enemy = pygame.Rect(enemy01_x,enemy01_y,64,64)
    return hit_enemy
    
