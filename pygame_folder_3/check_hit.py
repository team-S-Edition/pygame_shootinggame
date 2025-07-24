import pygame

# 味方の当たり判定チェック
def check_myplane(enemy_bombs, hit_myplane, screen,now_time,start_time,first_switch):
    for x,y in enemy_bombs:
        if hit_myplane.colliderect(x,y,10,10):
            if now_time-start_time>2000 and first_switch==False:#バグ対策
                enemy_bombs.remove([x,y])
                return True,False
        
    return False,True




# 敵の当たり判定チェック
def check_enemy(bombs, hit_enemy, screen, dokan_sound, bomb_effect_img):
    for x,y in bombs:
        if hit_enemy.colliderect(x,y,16,16):
            dokan_sound.play()
            screen.blit(bomb_effect_img, (x - bomb_effect_img.get_width() // 2, y - bomb_effect_img.get_height() // 2))
            pygame.display.update()
            bombs.remove([x, y])
            return True  # 当たったらTrueを返す
    return False  # 当たらなかったらFalse