import pygame

def enemy_move(enemy01_movemode,enemy01_x,width,speed):
        if 0>=enemy01_x:
            enemy01_movemode=1
        elif width-64<=enemy01_x:
            enemy01_movemode=0
        if enemy01_movemode==0:
            enemy01_x-=speed
        elif enemy01_movemode==1:
            enemy01_x+=speed

        return enemy01_x,enemy01_movemode