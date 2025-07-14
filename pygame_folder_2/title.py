import os
import pygame
import sys



def stage_status(screen):
     # クロック（FPS制御用）
    clock = pygame.time.Clock()

    
    # 画面サイズ
    info = pygame.display.Info()
    width = info.current_w
    height = info.current_h

    # フォント
    font_impact = pygame.font.SysFont("Impact", 65) # Impactフォント（大）
    font_impact2 = pygame.font.SysFont("Impact", 45) # Impactフォント（大）
    font_title = pygame.font.SysFont("msgothic", 60)  # ゴシック体 
    text2=font_impact2.render("PRESS SPACE TO START", True, (0, 0, 0))


    # 画像
    title_picture = pygame.image.load("title_picture.png")
    title_picture = pygame.transform.scale(title_picture,(width,height))
    title_rogo = pygame.image.load("タイトルロゴ.png")

    # アニメーション
    bar_height = 55 # バーの縦幅縦幅
    bar_y = height - bar_height -30 # バーのy座標
    bar2_y = 30
    bar_color = (0,153,153) # バーの色 0,204,51で#00cc33;　0,153,153で#009999;

    text2_width = text2.get_width() # テキストの横幅
    text2_x = 0 # 最初のテキストのx座標
    text_space = 50 # テキストの間隔
    total_width = text2_width + text_space # テキスト全体の横幅

    title_x = width - 750
    title_y = height/4



    running = True
     

    while running:

        for event in pygame.event.get(): # イベントを取得
            if event.type==pygame.KEYDOWN: # キーボードが押されたとき
                if event.key==pygame.K_ESCAPE: # 押されたキーがエスケープキーだった場合、ゲーム終了
                    return "ゲーム終了"
                if event.key == pygame.K_SPACE:
                    return "stage1"
                
         # 描画       
        screen.blit(title_picture,(0,0))
        screen.blit(title_rogo,(title_x,title_y))
        pygame.draw.rect(screen, bar_color, (0, bar_y, width, bar_height))
        pygame.draw.rect(screen, bar_color, (0, bar2_y, width, bar_height))

        new_text2_x = text2_x
        while new_text2_x < width:
            screen.blit(text2,(new_text2_x,bar_y)) 
            screen.blit(text2,(new_text2_x,bar2_y)) 
            new_text2_x += total_width

        text2_x -= 1
        
        if text2_x <= -total_width: 
            text2_x += total_width


        pygame.display.update()
        clock.tick(60)