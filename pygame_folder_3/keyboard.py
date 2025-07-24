import pygame    

def keyboard(myplane_x, myplane_y,speed):    
# キーボード操作の処理^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        keys = pygame.key.get_pressed()#キーボードが押されているかどうか
        if keys[pygame.K_LEFT]: #押されているキーボードが左矢印キーの場合
            myplane_x -= speed
        if keys[pygame.K_RIGHT]:#押されているキーボードが右矢印キーの場合
            myplane_x += speed
        if keys[pygame.K_UP]:
            myplane_y -= speed
        if keys[pygame.K_DOWN]:
            myplane_y += speed

            

        return myplane_x,myplane_y
