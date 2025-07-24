import pygame

def myplane_x_zahyou(myplane_x,width,myplane01):
    myplane_x = max(0, min(myplane_x, width - myplane01.get_width())) # 背景の端座標896
    return myplane_x

def myplane_y_zahyou(myplane_y,height,myplane01):
    myplane_y = max(0, min(myplane_y, height - myplane01.get_height()))
    return myplane_y

def enemy_x_zahyou(enemy01_x,width,enemy01):
    enemy01_x = max(0, min(enemy01_x, width - enemy01.get_width()))
    return enemy01_x

def enemy_y_zahyou(enemy01_y,height,enemy01):
    enemy01_y = max(0, min(enemy01_y, height - enemy01.get_height()))
    return enemy01_y