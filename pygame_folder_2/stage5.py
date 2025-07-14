#ライブラリのインポート
import pygame
import sys
import os
import time
import math
import serial


def stage_status(screen):
     # クロック（FPS制御用）
    clock = pygame.time.Clock()
    
    # タクトスイッチ受け取り
    switch = 1

    # スティック受け取り
    stick_x = 506
    stick_y = 507
    stick_center = 1    

    
    # 画面サイズ
    info = pygame.display.Info()
    total_width = info.current_w
    width = total_width - 300
    height = info.current_h

    #音声・BGM設定
    game_clear=pygame.mixer.Sound("game clear(voice).mp3")  # ファイル名に日本語があると失敗することあり
    gameover=pygame.mixer.Sound("game over(voice).mp3")
    dokan = pygame.mixer.Sound("dokka-nn(voice).mp3")

    
    # 画像の読み込み＆リサイズ
    ui = pygame.image.load("残弾数ui(日本語).png")
    ui = pygame.transform.scale(ui, (370, 370))
    background=pygame.image.load("背景(宇宙).png")
    background=pygame.transform.scale(background,(total_width,height))
    myplane01 = pygame.image.load("戦闘機.png")
    myplane01 = pygame.transform.scale(myplane01, (64, 64)) 
    bomb = pygame.image.load("ミサイル.png")
    bomb = pygame.transform.rotate(bomb, 180)
    bomb = pygame.transform.scale(bomb, (32, 32))
    enemy01 = pygame.image.load("敵戦闘機01.png")
    enemy01 = pygame.transform.scale(enemy01, (64, 64))
    enemy_bomb01_image=pygame.image.load("銃弾.png")
    enemy_bomb02_image=pygame.image.load("銃弾.png")
    angle = 180
    enemy_bomb01_image=pygame.transform.rotate(enemy_bomb01_image, angle)
    enemy_bomb01_image = pygame.transform.scale(enemy_bomb01_image, (25, 25))
    enemy_bomb02_image=pygame.transform.rotate(enemy_bomb02_image, angle)
    enemy_bomb02_image = pygame.transform.scale(enemy_bomb02_image, (25, 25))
    gameover_image=pygame.image.load("アスランもどき.png")
    gameover_image = pygame.transform.scale(gameover_image, (total_width, height))
    bomb_efect = pygame.image.load("爆発01.png")
    bomb_efect = pygame.transform.scale(bomb_efect, (64, 64))
    game_clear_image=pygame.image.load("完全勝利.png")
    game_clear_image = pygame.transform.scale(game_clear_image, (total_width, height))
    enemy02=pygame.image.load("戦闘妖精雪風.png")
    enemy02 = pygame.transform.scale(enemy02, (64, 64))


    
    # 初期位置＆スピード
    myplane_x, myplane_y = width // 2, height-64
    enemy01_x,enemy01_y= width // 2, 64
    enemy02_x,enemy02_y= width // 2, 128
    ui_x,ui_y = width,0
    speed = 5
    low_speed = 2
    enemy_speed = 3

    enemy2_speed = 8

    
    #flag初期設定
    gameclear_flag=False
    gameover_flag=False
    
    # 生存判定
    myplane_arrive = True
    enemy_arrive = True
    enemy2_arrive = True
    enemy_number = 2 # 敵の数

    
    # 銃弾関連変数初期設定
    bullet_count=10
    last_shot_time = 0
    shot_delay = 1000 # ディレイ時間（ミリ秒）
    now_time= 0
    last_bullet_time=0
    last_bullet_time2=0
    bombs=[]
    enemy_bombs01=[]
    new_enemy_bombs01=[]
    enemy_bombs02=[]
    new_enemy_bombs02=[]
    last_shot_time_enemy = 0
    enemy_bombs_speed = 8
    shot_delay_enemy = 1500
    shot_delay_enemy02 = 500


    # フォント
    font_stage1 = pygame.font.SysFont("msgothic", 75)

    font_impact = pygame.font.SysFont("Impact", 65) # Impactフォント（大）
    font_impact3 = pygame.font.SysFont("Impact", 55) # Impactフォント（中）
    font_impact2 = pygame.font.SysFont("Impact", 40) # Impactフォント（小）
    font_gothic = pygame.font.SysFont("msgothic",20) # ゴシック体
    font_text = pygame.font.SysFont("msgothic", 30)
    font_title = pygame.font.SysFont("msgothic", 60)
    font_stage1=pygame.font.SysFont("msgothic", 75)

    
    # テキスト
    text_stage4=font_stage1.render("ステージ5", True, (255, 255, 255))
    text_stage4_english =font_impact3.render("Stage5", True, (255, 255, 255))
    enemy_text = font_impact2.render(f"{enemy_number}", True, (0, 0, 0))  # ミサイルの数
    enemy_text = pygame.transform.rotate(enemy_text, -25)  # 10度回転
    setsumei_text = font_impact2.render(f"SPACE : SHOOT", True, (255,255,255)) # 操作方法説明
    setsumei_text2 = font_impact2.render(f"←↑↓→ : MOVE", True, (255,255,255))
    setsumei_text3 = font_text.render("スペースで次のステージへ",True ,(255,255,255))
    setsumei_text4 = font_text.render("Zキーでタイトル画面へ",True ,(255,255,255))
    setsumei_text5 = font_text.render("スペースでリスタート",True ,(255,255,255))
    setsumei_text6 = font_text.render("エスケープ(Esc)キーで終了",True ,(255,255,255))
    victory_text = font_impact2.render("VICTORY", True, (255,255,255))
    defeat_text = font_impact2.render("DEFEAT", True, (255,255,255))

    
    #その他
    enemy01_movemode=0
    enemy02_movemode=0
    first_switch=True
    now_time = 0
    running = True
    bullet_angle = 90

    # ポート番号
    com = "COM6"

    # シリアル通信
    ser = serial.Serial(com, 9600, timeout=1)
        
    

    while running:
        now_time = pygame.time.get_ticks() #現在時刻更新

            
        
# イベント処理------------------------------------------------------------------------------------------------------
        # 背景描画
        screen.blit(background,(0,0))
        for event in pygame.event.get():#エベントを取得
            if event.type == pygame.QUIT:#ウィンドウの「×」ボタンが押されたとき
                running=0
                break
            if event.type==pygame.KEYDOWN:#キーボードが押されたとき
                now_time = pygame.time.get_ticks()
                if event.key == pygame.K_SPACE:#押されたキーボードがスペースキーだった場合
                    if now_time - last_shot_time > shot_delay:
                        bullet_count-=1
                        bombs.append([myplane_x+16,myplane_y])#bombsというリストに[x+16,y]を追加
                        last_shot_time = now_time
                if event.key==pygame.K_ESCAPE:# 押されたキーがエスケープキーだった場合、ゲーム終了
                    return "ゲーム終了"

        
        # スティック入力受け取り
        try:
            if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8').strip()
                    if data:
                        parts = data.split(',')
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
        deadzone = 20
        
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


        keys = pygame.key.get_pressed()#キーボードが押されている間
        if keys[pygame.K_LEFT]:#押されているキーボードが左矢印キーの場合
            myplane_x -= speed
        if keys[pygame.K_RIGHT]:#押されているキーボードが右矢印キーの場合
            myplane_x += speed
        if keys[pygame.K_UP]:
            myplane_y -= speed
        if keys[pygame.K_DOWN]:
            myplane_y += speed
        
        if switch == 0:#スイッチ（引き金）が押されたとき
            if now_time - last_shot_time > shot_delay:
                bullet_count-=1
                bombs.append([myplane_x+16,myplane_y])#bombsというリストに[x+16,y]を追加
                last_shot_time = now_time
        

#---------------------------------------------------------------------------------------------------------------------
        new_bombs = []#new_bombsのリセット(中身を空にする)
        for x, y in bombs:
            y -= 3  # 移動速度
            if y >=0:  # 画面内なら残す
                screen.blit(bomb, (x, y))
                new_bombs.append([x, y])  # 更新された位置でリストに戻す
        bombs = new_bombs  # 更新
    
        hit_myplane=pygame.Rect(myplane_x, myplane_y, 64, 64)
        hit_enemy01=pygame.Rect(enemy01_x,enemy01_y,64,64)
        hit_enemy02=pygame.Rect(enemy02_x,enemy02_y,64,64)

#当たり判定制御--------------------------------------------------------------------------------------------------------------
        for x,y in bombs:
            if hit_enemy01.colliderect(x,y,16,16):
                gameclear_flag=True
                dokan.play()
                screen.blit(bomb_efect, (x - bomb_efect.get_width() // 2, y - bomb_efect.get_height() // 2))
                pygame.display.update()
                bombs.remove([x,y]) 
                enemy_arrive=False
                enemy2_arrive = False
            elif hit_enemy02.colliderect(x,y,16,16):
                gameclear_flag=True
                dokan.play()
                screen.blit(bomb_efect, (x - bomb_efect.get_width() // 2, y - bomb_efect.get_height() // 2))
                pygame.display.update()
                bombs.remove([x,y]) 
                enemy_arrive=False
                enemy2_arrive=False

        # 敵１の弾
        for x,y in enemy_bombs01:
            if hit_myplane.colliderect(x,y,10,10):
                if now_time - start_time > 2000 and not first_switch:
                    gameover_flag = True
                    enemy_bombs01.remove([x,y])
                    myplane_arrive = False

        if now_time - last_bullet_time > shot_delay_enemy:
            last_bullet_time = now_time  # ここはnow_timeで統一したほうがいい
            enemy_bombs01.append([enemy01_x, enemy01_y])

        new_enemy_bombs01 = []
        
        if enemy_arrive:
            for x, y in enemy_bombs01:
                y += 3
                if y <= height:
                    new_enemy_bombs01.append([x, y])

        enemy_bombs01 = new_enemy_bombs01

        for x, y in enemy_bombs01:
            screen.blit(enemy_bomb01_image, (x, y))


        #敵２の弾
        for x,y in enemy_bombs02:
            if hit_myplane.colliderect(x,y,10,10):
                if now_time-start_time>2000 and first_switch==False:#バグ対策
                    gameover_flag=True
                    enemy_bombs02.remove([x,y])
                    myplane_arrive=False

        if now_time-last_bullet_time2>shot_delay_enemy02:
            last_bullet_time2=pygame.time.get_ticks()
            enemy_bombs02.append([enemy02_x,enemy02_y])

        new_enemy_bombs02=[]
        if enemy2_arrive==True:
            for x,y in enemy_bombs02:
                y+= enemy_bombs_speed
                new_enemy_bombs02.append([x,y])
                if x < 0 or width < x and y < 0 or height < y:
                    new_enemy_bombs02.remove([x,y])

            enemy_bombs02=new_enemy_bombs02#更新
            
            for x, y in enemy_bombs02:
                screen.blit(enemy_bomb02_image, (x, y))
        
        #動き
        if 0>=enemy01_x:
            enemy01_movemode=1
        elif width-64<=enemy01_x:
            enemy01_movemode=0

        if 0>=enemy02_x:
            enemy02_movemode=1
        elif width-64<=enemy02_x:
            enemy02_movemode=0

        if enemy01_movemode==0:
            enemy01_x-=4
        elif enemy01_movemode==1:
            enemy01_x+=4

        if enemy02_movemode==0:
            enemy02_x-= enemy2_speed
        elif enemy02_movemode==1:
            enemy02_x+= enemy2_speed

    # 画面外に出ないようにする
    #*if myplane_x<0:
     #   myplane_x=0
    #elif myplane_x>width-myplane01.get_width():
     #   myplane_x=width-myplane01.get_width()*\
        myplane_x = max(0, min(myplane_x, width - myplane01.get_width())) # 背景の端座標896
        myplane_y = max(0, min(myplane_y, height - myplane01.get_height()))
        enemy01_x = max(0, min(enemy01_x, width - enemy01.get_width())) # 背景の端座標896
        enemy01_y = max(0, min(enemy01_y, height - enemy01.get_height()))
        enemy02_x = max(0, min(enemy02_x, width - enemy02.get_width())) # 背景の端座標896
        enemy02_y = max(0, min(enemy02_y, height - enemy02.get_height()))

    # 描画
        pygame.draw.rect(screen, (128,128,128), (width, 0, 300, height))
        screen.blit(ui, (ui_x,ui_y))
        if myplane_arrive:
            screen.blit(myplane01, (myplane_x, myplane_y))
        else:
            gameover_flag=True
        if enemy_arrive:
            screen.blit(enemy01,(enemy01_x,enemy01_y))
        if enemy2_arrive:
            screen.blit(enemy02,(enemy02_x,enemy02_y))
            
        bombs_text = font_impact.render(f"{bullet_count}", True, (0, 0, 0))  # ミサイルの数
        bombs_text = pygame.transform.rotate(bombs_text, 10)  # 10度回転
        screen.blit(bombs_text, (ui_x+200, ui_y+45))  # 2桁のとき左寄り  
        screen.blit(setsumei_text,(width+30, 300))
        screen.blit(setsumei_text2,(width+30, 350))
        screen.blit(enemy_text,(ui_x+170, ui_y+170))


        if first_switch==True:#最初だけ処理される　ステージ名表示
            for i in range(1, height,40):
                screen.fill((0,0,0,))
                pygame.draw.rect(screen, (128,128,128), (0, height - i, total_width, height))
                pygame.time.delay(50)
                pygame.display.update()
            screen.blit(text_stage4,(total_width/6,height/2))
            screen.blit(text_stage4_english,(total_width/6,height/2 + 80))
            pygame.display.update()
            time.sleep(2.5)
            start_time=pygame.time.get_ticks()
            first_switch = False


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
            screen.blit(defeat_text,(total_width/2 + 50,height*2/3 + 50))
            screen.blit(setsumei_text5,(total_width/2 + 50,height*2/3 + 100))
            screen.blit(setsumei_text4,(total_width/2 + 50,height*2/3 + 150))
            screen.blit(setsumei_text6,(total_width/2 + 50,height*2/3 + 200))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            return "stage5"
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
            screen.blit(victory_text,(total_width/2 + 50,height*2/3 + 50))
            screen.blit(setsumei_text3,(total_width/2 + 50,height*2/3 + 100))
            screen.blit(setsumei_text4,(total_width/2 + 50,height*2/3 + 150))
            screen.blit(setsumei_text6,(total_width/2 + 50,height*2/3 + 200))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            return "stage6"
                        if event.key == pygame.K_z:
                            return "title"
                        if event.key == pygame.K_ESCAPE:
                            return "ゲーム終了"
                        

        
        pygame.display.update()
        clock.tick(60)
