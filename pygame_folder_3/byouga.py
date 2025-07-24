import pygame


def byouga(myplane_arrive,screen,myplane01,myplane_x,myplane_y):
        if myplane_arrive:
            screen.blit(myplane01, (myplane_x, myplane_y))
        else:
            gameover_flag=True