# ライブラリ・モジュール
import os
import pygame
import sys
import time
import math

# ステージファイル
import title
import stage1

# 初期化
pygame.init()

#タイトル名
pygame.display.set_caption("シューティングゲーム")

# プログラムを使ってるファイルから探す
os.chdir(os.path.dirname(__file__))

# ステージ制御
stage = "stage1"

# 画面サイズ
info = pygame.display.Info()
all_width=info.current_w
width = info.current_w-300
height = info.current_h
width2 = (info.current_w-300)/2
height2 = info.current_h/2
screen = pygame.display.set_mode((width+300, height))

while True:
    if stage == "ゲーム終了":
        break
    if stage == "title":
        stage = title.stage_status(screen)
    if stage == "stage1":
        stage = stage1.stage_status(screen)


