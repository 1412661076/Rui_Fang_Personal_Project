"""
  Capstone Project.  Code written by Rui Fang.
  Fall term, 2018-2019.
"""

import time
import rosebotics_even_newer as rb
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import turtle
import math
import random
from PIL import Image, ImageTk

mqtt_client = com.MqttClient()
mqtt_client.connect('fr', 'robo32')
time.sleep(1)

count1 = 0
count2 = 0
count3 = 0


class HP(object):
    def __init__(self):
        self.hp = 4

    def __str__(self):
        return str(self.hp)

    def lose(self, n):
        self.hp -= n
        if self.hp <= 0:
            self.hp = 0


class Counter(object):
    def __init__(self):
        self.number = 0

    def add(self, n):
        self.number += n


def main():
    run_window()

    

def run_window():
    hp = HP()
    frnb = tkinter.Tk()
    frnb.title('Robot Adventure')
    frnb.geometry('960x720+250+35')

    background = tkinter.PhotoImage(file='bg.gif')
    ttk.Button(frnb, image=background).place(x=0, y=0)

    canva = tkinter.Canvas(frnb, width=600, height=600)
    canva.place(x=180,y=0)

    randxlist = []
    randylist = []
    for k in range(16):
        randx = random.randrange(-300, 300)
        randy = random.randrange(-300, 300)
        randxlist += [randx]
        randylist += [randy]

    dot = turtle.RawTurtle(canva, 'arrow')
    dot.left(90)

    coin = Counter()
    c = tkinter.StringVar()
    c.set('Now you have {} coins'.format(coin.number))
    coin_lable = tkinter.Label(frnb, textvariable=c, font=24)
    coin_lable.place(x=385, y=605)

    hp4 = 'progress_bar_100.gif'
    hp3 = 'progress_bar_75.gif'
    hp2 = 'progress_bar_50.gif'
    hp1 = 'progress_bar_25.gif'
    hp0 = 'progress_bar_0.gif'
    frnb.hp4 = ImageTk.PhotoImage(Image.open(hp4))
    frnb.hp3 = ImageTk.PhotoImage(Image.open(hp3))
    frnb.hp2 = ImageTk.PhotoImage(Image.open(hp2))
    frnb.hp1 = ImageTk.PhotoImage(Image.open(hp1))
    frnb.hp0 = ImageTk.PhotoImage(Image.open(hp0))

    btn_label = tkinter.Label(frnb, image=frnb.hp4)
    btn_label.place(x=780, y=600)

    hp_lable = tkinter.Label(frnb, text='Your current HP', font=24)
    hp_lable.place(x=780, y=580)

    count = Counter()

    bombimg = tkinter.PhotoImage(file='bomb.gif')
    coinimg = tkinter.PhotoImage(file='coin.gif')
    trapimg = tkinter.PhotoImage(file='warning.gif')
    heartimg = tkinter.PhotoImage(file='heart_small.gif')
    treasure = tkinter.PhotoImage(file='q.gif')
    canva.create_image(randxlist[0], randylist[0], image=bombimg)
    canva.create_image(randxlist[1], randylist[1], image=bombimg)
    canva.create_image(randxlist[2], randylist[2], image=bombimg)
    canva.create_image(randxlist[3], randylist[3], image=bombimg)
    canva.create_image(randxlist[4], randylist[4], image=bombimg)

    canva.create_image(randxlist[5], randylist[5], image=coinimg)
    canva.create_image(randxlist[6], randylist[6], image=coinimg)
    canva.create_image(randxlist[7], randylist[7], image=coinimg)
    canva.create_image(randxlist[8], randylist[8], image=coinimg)
    canva.create_image(randxlist[9], randylist[9], image=coinimg)

    canva.create_image(randxlist[10], randylist[10], image=trapimg)
    canva.create_image(randxlist[11], randylist[11], image=trapimg)
    canva.create_image(randxlist[12], randylist[12], image=trapimg)
    canva.create_image(randxlist[13], randylist[13], image=trapimg)

    canva.create_image(randxlist[14], randylist[14], image=heartimg)

    frnb.bind('<Key-w>', lambda event: go_straight(dot, 12, randxlist, randylist, hp, btn_label, frnb, count, coin, c, canva))
    frnb.bind('<Key-a>', lambda event: turn_degree(dot, 9))
    frnb.bind('<Key-s>', lambda event: go_straight(dot, -12, randxlist, randylist, hp, btn_label, frnb, count, coin, c, canva))
    frnb.bind('<Key-d>', lambda event: turn_degree(dot, -9))

    frnb.bind('<KeyRelease-w>', lambda event: w_release())
    frnb.bind('<KeyRelease-a>', lambda event: a_release())
    frnb.bind('<KeyRelease-s>', lambda event: s_release())
    frnb.bind('<KeyRelease-d>', lambda event: d_release())
    frnb.bind('<Key-1>', lambda event: hp_lose(hp, btn_label, frnb, count, 1))

    frnb.mainloop()


def change_pic(lbl, frnb, count):
    if count.number == 1:
        lbl.configure(image=frnb.hp3)
    elif count.number == 2:
        lbl.configure(image=frnb.hp2)
    elif count.number == 3:
        lbl.configure(image=frnb.hp1)
    elif count.number == 4:
        lbl.configure(image=frnb.hp0)
        you_lose(frnb)


def hp_lose(hp, lbl, frnb, count, n):
    hp.lose(n)
    count.add(n)
    change_pic(lbl, frnb, count)
    if n == -1:
        mqtt_client.send_message('calibrate')
        print('Repairing')


def go_straight(turt, dist, randxlist, randylist, hp, btn_label, frnb, count, coin, c, canva):
    global count1
    turt.forward(dist)
    count1 += 1
    for k in range(5):
        if turt.xcor() <= randxlist[k] + 15 and turt.xcor() >= randxlist[k] - 15 and -turt.ycor() <= randylist[
            k] + 15 and -turt.ycor() >= randylist[k] - 15:
            randxlist[k] = 1000
            randylist[k] = 1000
            hp_lose(hp, btn_label, frnb, count, 1)

    for i in range(5, 10):
        if turt.xcor() <= randxlist[i] + 15 and turt.xcor() >= randxlist[i] - 15 and -turt.ycor() <= randylist[
            i] + 15 and -turt.ycor() >= randylist[i] - 15:
            get_coin(coin, c, randxlist, randylist, i, frnb, canva)

    for j in range(10, 14):
        if turt.xcor() <= randxlist[j] + 15 and turt.xcor() >= randxlist[j] - 15 and -turt.ycor() <= randylist[
            j] + 15 and -turt.ycor() >= randylist[j] - 15:
            randylist[j] = 1000
            randxlist[j] = 1000
            get_trapped(turt)


    if turt.xcor() <= randxlist[14] + 15 and turt.xcor() >= randxlist[14] - 15 and -turt.ycor() <= randylist[
        14] + 15 and -turt.ycor() >= randylist[14] - 15:
        hp_lose(hp, btn_label, frnb, count, -1)
        randxlist[14] = 1000
        randylist[14] = 1000


def w_release():
    global count1
    distance = count1 * 12
    mqtt_client.send_message('go_straight', [distance])
    count1 = 0

def s_release():
    global count1
    distance = -(count1 * 12)
    mqtt_client.send_message('go_straight', [distance])
    count1 = 0

def turn_degree(turt, deg):
    global count2
    turt.left(deg)
    count2 += 1

def a_release():
    global count2
    angle = -(count2 * 9)
    mqtt_client.send_message('turn_angle', [angle])
    count2 = 0

def d_release():
    global count2
    angle = count2 * 9
    mqtt_client.send_message('turn_angle', [angle])
    count2 = 0

def get_coin(coin, c, xlist, ylist, i, frnb, root):
    coin.number += 1
    c.set('Now you have {} coins'.format(coin.number))
    mqtt_client.send_message('get_coin')
    print('Yeah! You\'ve found a coin! Now you have {} coins'.format(coin.number))
    xlist[i] = 1000
    ylist[i] = 1000
    if coin.number >= 5:
        you_win(frnb, root)

def get_trapped(turt):
    print('Oh no! Your robot is trapped!')
    turt.left(1800)
    mqtt_client.send_message('get_trapped')

def you_win(frnb, root):
    mqtt_client.send_message('you_win')
    win = tkinter.PhotoImage(file='win.gif')
    root.create_image(0, 0, image=win)
    time.sleep(3)

    frnb.destroy()

def you_lose(frnb):
    print('You lose :(')
    mqtt_client.send_message('you_lose')
    time.sleep(3)
    frnb.destroy()

main()
