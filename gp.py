#!/usr/bin/env python3
from pygame.locals import *
from scipy import signal
import pygame
import sys
import numpy as np
import os
import binascii
import subprocess


width=8
height=8
scale=16
win_id=""

def getwindowid():
    try:
        # ウィンドウidを取得
        w_id = subprocess.check_output(
            ["xdotool", "getactivewindow"]
        ).splitlines()[0]
        return w_id

    except subprocess.CalledProcessError:
        return "0"


def focus_window(id):
    try:
        # フォーカスを移動
        subprocess.run(["xdotool", "windowactivate", id])
        return True
    except subprocess.CalledProcessError:
        return False


def draw_grid(screen):
  screen.fill((0,0,0))
  for i in range(width):
    pygame.draw.line(screen,(0,255,0),(i*scale,0),(i*scale,scale*height),1)
  for i in range(height):
    pygame.draw.line(screen,(0,255,0),(0,i*scale),(scale*width,i*scale),1)

def set(screen,cx,cy,c):
  screen.fill((c*255,c*255,c*255),(cx*scale+1,cy*scale+1,scale-1,scale-1))

def put(F,screen):
  for i in range(len(F)):
    for j in range(len(F[1])):
       set(screen,j,i,F[i][j])

def rev(F,cx,cy):
  F[cy][cx]=int(F[cy][cx])^1
  return(F)

def clear():
    return(np.zeros((height,width)))

def setscr():
    pygame.quit()
    pygame.init()    # Pygameを初期化
    screen = pygame.display.set_mode((scale*width,scale*height))   # 画面を作成
    s="gp "+str(width)+"x"+str(height)
    pygame.display.set_caption(s)    # タイトルを作成
    draw_grid(screen)
    return screen

def eventloop(F,screen):
    global width,height,win_id
    run='e'
    while run!='q' and run!='w':
        for event in pygame.event.get():
            if event.type == QUIT:
                run='q'
            if event.type == KEYDOWN:  # キーを押したとき
                k=pygame.key.name(event.key)
                if k== 'q':
                    run='q'
                if k== 'w':
                    run='w'
                elif k=='z':
                    focus_window(win_id)
                    width=int(input("Input width:"))
                    height=int(input("Input height:"))
                    screen=setscr()
                    F=clear()
                elif k=='c':
                    F=clear()
                    put(F,screen)
            elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    F=rev(F,x//scale,y//scale)
                    put(F,screen)
            elif event.type == MOUSEMOTION:
                    x, y = event.pos
        pygame.display.update()
    return run,F

def main():
    global height,width,win_id
    fn=sys.argv[1]
    win_id=getwindowid()
    screen=setscr()
    F=clear()
    put(F,screen)
    if os.path.exists(fn):
        try:
            F = np.loadtxt(fn)
        except:
            print("File format wrong.")
            F = clear()
        height=len(F)
        width=len(F[0])
        screen=setscr()
        put(F,screen)
        print(f"width: {width} height: {height}")
    flag,F=eventloop(F,screen)
    if flag=='w':
        np.savetxt(fn, F, "%d")
        print("File written.");
    else:
        print("File is not written.")
    pygame.quit()
    sys.exit()

if __name__=='__main__':
    main()

