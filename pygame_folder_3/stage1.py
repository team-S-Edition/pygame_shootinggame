#ライブラリのインポート ※触らないで！
import pygame
import sys
import os
import time
import math
import serial

import keyboard
import hit
import check_hit
import bomb_shot
import enemy_move
import zahyou_chousei


def stage_status(screen):
     # クロック（FPS制御用）※触らないで！
    clock = pygame.time.Clock()

    # スティック受け取り ※触らないで！
    stick_x = 506
    stick_y = 507
    stick_center = 1   

    # タクトスイッチ受け取り ※触らないで！
    switch = 1

    
    # 画面サイズ ※触らないで！
    info = pygame.display.Info()
    total_width = info.current_w
    width = total_width - 300
    height = info.current_h

    #音声・BGM設定
    game_clear=pygame.mixer.Sound("game clear(voice).mp3")  # ファイル名に日本語があると失敗することあり
    gameover=pygame.mixer.Sound("game over(voice).mp3")
    dokan = pygame.mixer.Sound("dokka-nn(voice).mp3")

    
    # 画像の読み込み＆リサイズ
    # 残弾数UI
    ui = pygame.image.load("残弾数ui(日本語).png")
    ui = pygame.transform.scale(ui, (370, 370))

    # 背景
    background = pygame.image.load("背景(宇宙).png")
    background = pygame.transform.scale(background,(total_width,height))

    # 自機
    myplane01 = pygame.image.load("戦闘機.png")
    myplane01 = pygame.transform.scale(myplane01, (64, 64)) 

    # 自機の弾
    bomb = pygame.image.load("ミサイル.png")
    bomb = pygame.transform.rotate(bomb, 180)
    bomb = pygame.transform.scale(bomb, (32, 32))

    # 敵機１
    enemy01 = pygame.image.load("敵戦闘機01.png")
    enemy01 = pygame.transform.scale(enemy01, (64, 64))

    # 敵機２
    enemy02 = pygame.image.load("中ボス.png")
    enemy02 = pygame.transform.scale(enemy02, (64, 64))

    # 敵機３
    enemy03 = pygame.image.load("戦闘妖精雪風.png")
    enemy03 = pygame.transform.scale(enemy03, (64, 64))

    # 敵機の弾
    enemy_bomb01_image=pygame.image.load("銃弾.png")
    enemy_bomb01_image = pygame.transform.scale(enemy_bomb01_image, (25, 25))

    # ゲームオーバー画面
    gameover_image=pygame.image.load("アスランもどき.png")
    gameover_image = pygame.transform.scale(gameover_image, (total_width, height))

    # 爆発エフェクト
    bomb_efect = pygame.image.load("爆発01.png")
    bomb_efect = pygame.transform.scale(bomb_efect, (64, 64))

    # 勝利画面
    game_clear_image=pygame.image.load("完全勝利.png")
    game_clear_image = pygame.transform.scale(game_clear_image, (total_width, height))
    
    angle = 180 # 弾の角度を変えるときに使う用
    
    # 初期位置＆スピード
    myplane_x, myplane_y = width // 2, height-64
    enemy01_x,enemy01_y= width // 2, 64
    ui_x,ui_y = width,0
    speed = 5
    low_speed = 2
    enemy_speed = 3

    
    #flag初期設定 
    gameclear_flag=False
    gameover_flag=False
    
    # 生存判定
    myplane_arrive = True
    enemy_arrive = True
    enemy_number = 1 # 敵の数

    
    # 銃弾関連変数初期設定
    bullet_count=10 #弾数
    last_shot_time = 0 #最後に弾を撃った時間（自機）
    shot_delay = 1000 # ディレイ時間（ミリ秒/自機）
    now_time= 0 # 現在時刻
    last_bullet_time=0 # 最後に弾を撃った時間（敵機）
    bombs=[] # 弾のリスト（自機）
    new_bombs=[]
    enemy_bombs01=[] # 弾のリスト（敵機）
    new_enemy_bombs01=[] # 弾のリスト（敵機）
    shot_delay_enemy = 1000 # ディレイ時間（ミリ秒/敵機）


    # フォント
    font_impact = pygame.font.SysFont("Impact", 65) # Impactフォント（大）
    font_impact3 = pygame.font.SysFont("Impact", 55) # Impactフォント（中）
    font_impact2 = pygame.font.SysFont("Impact", 40) # Impactフォント（小）
    font_gothic = pygame.font.SysFont("msgothic",20) # ゴシック体（小）
    font_text = pygame.font.SysFont("msgothic", 30) # ゴシック体（中）
    font_title = pygame.font.SysFont("msgothic", 60) # ゴシック体（大）
    font_stage1=pygame.font.SysFont("msgothic", 75) # ゴシック体（特大）

    
    # テキスト
    text_stage1=font_stage1.render("ステージ１", True, (255, 255, 255) )# タイトル文字
    text_stage1_english =font_impact2.render("Stage1", True, (255, 255, 255)) # タイトル文字（英語）
    enemy_text = font_impact2.render(f"{enemy_number}", True, (0, 0, 0))  # ミサイルの数
    enemy_text = pygame.transform.rotate(enemy_text, -25)  # 10度回転
    setsumei_text = font_impact2.render(f"SPACE : SHOOT", True, (255,255,255)) # 操作方法説明
    setsumei_text2 = font_impact2.render(f"←↑↓→ : MOVE", True, (255,255,255))
    setsumei_text3 = font_text.render("スペースで次のステージへ",True ,(255,255,255))
    setsumei_text4 = font_text.render("Zキーでタイトル画面へ",True ,(255,255,255))
    setsumei_text5 = font_text.render("スペースでリスタート",True ,(255,255,255))
    setsumei_text6 = font_text.render("エスケープ(Esc)キーで終了",True ,(255,255,255))
    victory_text = font_impact3.render("VICTORY", True, (255,255,255))
    defeat_text = font_impact3.render("DEFEAT", True, (255,255,255))

    
    #その他
    enemy01_movemode=0
    first_switch=True
    now_time = 0
    running = True

    # ポート番号 ※触らないで！
    com = "COM6"
    """
    #シリアル通信 ※触らないで！
    ser = serial.Serial(com, 9600, timeout=1)
    """

    # メインループ
    while running: 
        now_time = pygame.time.get_ticks() #現在時刻更新 ※触らないで！
        
        if first_switch==True:#最初だけ処理される　ステージ名表示
            for i in range(1, height,40):
                screen.fill((0,0,0,))
                pygame.draw.rect(screen, (128,128,128), (0, height - i, total_width, height))
                pygame.time.delay(50)
                pygame.display.update()
            screen.blit(text_stage1,(total_width/6,height/2))
            screen.blit(text_stage1_english,(total_width/6,height/2 + 80))
            pygame.display.update()
            time.sleep(2.5)
            start_time=pygame.time.get_ticks()
            first_switch = False

            
        
# イベント処理------------------------------------------------------------------------------------------------------
        # 背景描画
        screen.blit(background,(0,0))

        # イベント取得
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # ウィンドウの「×」ボタンが押されたとき
                running=0
                break # ループ脱出
            if event.type==pygame.KEYDOWN: # キーボードが押されたとき
                if event.key == pygame.K_SPACE:#押されたキーボードがスペースキーだった場合
                    if now_time - last_shot_time > shot_delay: 
                        bullet_count-=1
                        bombs.append([myplane_x+16,myplane_y])#bombsというリストに[x+16,y]を追加
                        last_shot_time = now_time
                if event.key==pygame.K_ESCAPE:# 押されたキーがエスケープキーだった場合、ゲーム終了
                    return "ゲーム終了"

        """
        # スティック・タクトスイッチ入力受け取り ※触らないで！
        try:
            if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8').strip()
                    if data:
                        parts = data.split(',')
                        if len(parts) >= 4:
                            stick_x = int(parts[0]) # スティックx座標
                            stick_y = int(parts[1]) # スティックy座標
                            stick_center = int(parts[2]) # スティック押し込み
                            switch = int(parts[3]) # スイッチ押し込み
                            print(f"x={stick_x}, y={stick_y}, center={stick_center}, switch={switch}")
        except KeyboardInterrupt:
            ser.close()
        
        # スティック入力処理 x中心:506 y中心:507 スティック押し込み:1 スティック入力が反応しない範囲(deadzone):±20
        x_tyusin = 506
        y_tyusin = 507
        deadzone = 10
        
        # x方向
        if stick_x < x_tyusin - deadzone * 5:
            myplane_x -= speed
        elif stick_x < x_tyusin - deadzone:
            myplane_x -= low_speed
        elif stick_x > x_tyusin + deadzone *5:
            myplane_x += speed
        elif stick_x > x_tyusin + deadzone:
            myplane_x += low_speed

         # y方向
        if stick_y < y_tyusin - deadzone * 5:
            myplane_y -= speed
        elif stick_y < y_tyusin - deadzone:
            myplane_y -= low_speed
        elif stick_y > y_tyusin + deadzone * 5:
            myplane_y += speed
        elif stick_y > y_tyusin + deadzone:
            myplane_y += low_speed

        
        if switch == 0:#スイッチ（引き金）が押されたとき
            if now_time - last_shot_time > shot_delay:
                bullet_count-=1
                bombs.append([myplane_x+16,myplane_y])#bombsというリストに[x+16,y]を追加
                last_shot_time = now_time
        """

        myplane_x, myplane_y = keyboard.keyboard(myplane_x, myplane_y, speed)
#---------------------------------------------------------------------------------------------------------------------
    
        # 当たり判定制御
        hit_myplane=hit.hit_myplane(myplane_x, myplane_y)
        hit_enemy01=hit.hit_enemy(enemy01_x,enemy01_y)

        # 敵に味方の弾が当たった時
        gameclear_flag = check_hit.check_enemy(bombs,hit_enemy01,screen,dokan,bomb_efect)

        # 味方に敵の弾が当たったとき
        gameover_flag,myplane_arrive = check_hit.check_myplane(enemy_bombs01,hit_myplane,screen,now_time,start_time,first_switch)

        # 自機弾の移動プログラム
        bombs = bomb_shot.bombs(bombs,new_bombs,screen,bomb)  # 更新

        # 敵弾の移動プログラム
        enemy_bombs01, last_bullet_time = bomb_shot.enemy_bombs(enemy_bombs01,now_time,shot_delay_enemy,enemy01_x,enemy01_y,enemy_arrive,height,screen,enemy_bomb01_image,last_bullet_time)
        
        #動き^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        enemy01_x,enemy01_movemode = enemy_move.enemy_move(enemy01_movemode,enemy01_x,width,enemy_speed)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # 画面外に出ないようにする
    #*if myplane_x<0:
     #   myplane_x=0
    #elif myplane_x>width-myplane01.get_width():
     #   myplane_x=width-myplane01.get_width()*\
        myplane_x = zahyou_chousei.myplane_x_zahyou(myplane_x,width,myplane01) # 背景の端座標896
        myplane_y = zahyou_chousei.myplane_y_zahyou(myplane_y,height,myplane01)
        enemy01_x = zahyou_chousei.enemy_x_zahyou(enemy01_x,width,enemy01) # 背景の端座標896
        enemy01_y = zahyou_chousei.enemy_y_zahyou(enemy01_y,height,enemy01)

    # 描画
        pygame.draw.rect(screen, (128,128,128), (width, 0, 300, height))
        screen.blit(ui, (ui_x,ui_y))
        if myplane_arrive:
            screen.blit(myplane01, (myplane_x, myplane_y))
        else:
            gameover_flag=True
        if enemy_arrive:
            screen.blit(enemy01,(enemy01_x,enemy01_y))
            
        bombs_text = font_impact.render(f"{bullet_count}", True, (0, 0, 0))  # ミサイルの数
        bombs_text = pygame.transform.rotate(bombs_text, 10)  # 10度回転
        screen.blit(bombs_text, (ui_x+200, ui_y+45))  # 2桁のとき左寄り  
        screen.blit(setsumei_text,(width+30, 300))
        screen.blit(setsumei_text2,(width+30, 350))
        screen.blit(enemy_text,(ui_x+170, ui_y+170))





        if(bullet_count<1):
            running=1
            gameover_flag=True 

        if gameover_flag==True:
            screen.blit(gameover_image,(0,0))
            pygame.display.update()
            gameover.play()
            time.sleep(2)

            for i in range(total_width, int(total_width/2) , -20):
                pygame.draw.rect(screen, (128,128,128), (i, height*2/3, 100, height))
                pygame.time.delay(10)
                pygame.display.update()
            screen.blit(defeat_text,(total_width/2 + 50,height*2/3 + 30))
            screen.blit(setsumei_text5,(total_width/2 + 50,height*2/3 + 100))
            screen.blit(setsumei_text4,(total_width/2 + 50,height*2/3 + 150))
            screen.blit(setsumei_text6,(total_width/2 + 50,height*2/3 + 200))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            return "stage1"
                        if event.key == pygame.K_z:
                            return "title"
                        if event.key == pygame.K_ESCAPE:
                            return "ゲーム終了"
        
        if gameclear_flag==True:
            time.sleep(1)
            screen.blit(game_clear_image,(0,0))
            pygame.display.update()
            game_clear.play()
            time.sleep(2)
            for i in range(total_width, int(total_width/2) , -20):
                pygame.draw.rect(screen, (128,128,128), (i, height*2/3, 100, height))
                pygame.time.delay(10)
                pygame.display.update()
            screen.blit(victory_text,(total_width/2 + 50,height*2/3 + 30))
            screen.blit(setsumei_text3,(total_width/2 + 50,height*2/3 + 100))
            screen.blit(setsumei_text4,(total_width/2 + 50,height*2/3 + 150))
            screen.blit(setsumei_text6,(total_width/2 + 50,height*2/3 + 200))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            return "stage1"
                        if event.key == pygame.K_z:
                            return "title"
                        if event.key == pygame.K_ESCAPE:
                            return "ゲーム終了"

        
        pygame.display.update()
        clock.tick(60)


