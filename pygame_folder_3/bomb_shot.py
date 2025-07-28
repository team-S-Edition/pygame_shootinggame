import pygame

def bombs(bombs,new_bombs,screen,bomb,speed):
    new_bombs = []#new_bombsのリセット(中身を空にする)
    for x, y in bombs:
        y -= speed  # 移動速度
        if y >=0:  # 画面内なら残す
            screen.blit(bomb, (x, y))
            new_bombs.append([x, y])  # 更新された位置でリストに戻す
    bombs = new_bombs  # 更新

    return new_bombs

def enemy_bombs(enemy_bombs01, now_time, shot_delay_enemy, enemy01_x, enemy01_y, enemy_arrive, height, screen, enemy_bomb01_image, last_bullet_time,speed):
    if now_time - last_bullet_time > shot_delay_enemy:
        last_bullet_time = pygame.time.get_ticks()
        enemy_bombs01.append([enemy01_x, enemy01_y])

    new_enemy_bombs01 = []
    if enemy_arrive:
        for x, y in enemy_bombs01:
            y += speed  # 移動速度
            new_enemy_bombs01.append([x, y])
            if y > height:
                new_enemy_bombs01.remove([x, y])

        enemy_bombs01 = new_enemy_bombs01

        for x, y in enemy_bombs01:
            screen.blit(enemy_bomb01_image, (x, y))

    return enemy_bombs01, last_bullet_time
