# 猜拳游戏的gui界面
import copy
import tkinter
import numpy as np
from tkinter import *
import cv2
from PIL import Image, ImageTk
import new
import random

root = Tk()
root.geometry('1000x600')  # 设置窗口大小及位置
root.resizable(0, 0)

cap = cv2.VideoCapture(0)  # 获得视频输出
cap_region_x_begin = 0.5
cap_region_y_end = 0.8
isBgCaptured = 0
cnt = -1


class Game:
    rank=Label()
    def __init__(self):
        self.game = Frame(root, bg='#F5F5F5')
        self.game.pack(fill=BOTH, expand=True)

        title = Label(self.game, text='猜拳', font=('微软雅黑', 40), bg='#F5F5F5', fg='#263238')
        title.pack(pady=50)

        start_btn = Button(self.game, text='开始游戏', width=20, height=2, font=('微软雅黑', 16),
                           bg='#E6A23C', fg='white', activebackground='#FFB900',
                           relief='flat', overrelief='raised', command=self.GameStart)
        start_btn.pack(pady=10)

        quit_btn = Button(self.game, text='退出游戏', width=20, height=2, font=('微软雅黑', 16),
                          bg='#909399', fg='white', activebackground='#A6A6A6',
                          relief='flat', overrelief='raised', command=self.GameQuit)
        quit_btn.pack(pady=10)

        self.rank = Label(self.game, text='筹码记录', font=('微软雅黑', 40), bg='#F5F5F5', fg='#263238')
        self.rank.pack(pady=50)
        file=open('rank','r')
        self.rank["text"]="记录："+file.read()
        file.close()

        root.mainloop()

    def GameStart(self):
        game_help = Frame(self.game, bg='#37474F')
        game_help.place(width=600, height=300, x=200, y=150)

        title_bar = Frame(game_help, bg='#546E7A')
        title_bar.pack(fill=X)
        title = Label(title_bar, text='帮助', bg='#546E7A', fg='white', font=('微软雅黑', 20))
        title.grid(row=0, column=0)
        back_btn = Button(title_bar, text='返回', width=5, height=2, font=('微软雅黑', 14),
                          bg='#546E7A', fg='white', activebackground='#78909C',
                          relief='flat', overrelief='raised', command=lambda: game_help.destroy())
        back_btn.grid(row=0, column=1)
        title_bar.columnconfigure(0, weight=1)

        content = Label(game_help, bg='#37474F', fg='white', font=('微软雅黑', 12),
                        text='欢迎来到赌徒游戏！\n\n在开始游戏前，请先校准背景，按下“确定”按钮。'
                             '\n\n游戏会在三秒钟后自动开始。\n\nTIPS:不出拳会默认帮你出石头哦')
        content.pack(expand=True, pady=10)

        confirm_btn = Button(game_help, text='确定', width=10, height=2, font=('微软雅黑', 16),
                             bg='#E1F5FE', fg='#546E7A', activebackground='#78909C',
                             relief='flat', overrelief='raised', command=lambda: start())
        confirm_btn.pack(pady=15)

        def start():
            root.withdraw()#按下确定隐藏主页面
            game_help.destroy()
            video = Toplevel(self.game)
            video.geometry('800x800')
            App(video)
            tips = Label(video, bg='#37474F', fg='white', font=('微软雅黑', 16),
                         text='确保方框中没有多余的可移动事物后点击开始进行游戏\n\nTIPS:包括你的头哦，还有尽量在干净的背景下进行游戏')
            tips.pack(pady=10)
            rules = Label(video, bg='#37474F', fg='white', font=('微软雅黑', 16),
                         text='平局加10筹码！赢下一场筹码以指数翻倍！输掉一场失去所有的筹码！')
            rules.pack(pady=10)
            btn_group = Frame(video)
            btn_group.pack()
            btn_ok = Button(btn_group, text='开始', width=20, height=2, font=('微软雅黑', 16),
                            bg='#E6A23C', fg='white', activebackground='#FFB900',
                            relief='flat', overrelief='raised', command=lambda: cf(video))
            btn_ok.grid(row=0, column=0)
            btn_exit = Button(btn_group, text='返回', width=20, height=2, font=('微软雅黑', 16),
                              bg='#E6A23C', fg='white', activebackground='#FFB900',
                              relief='flat', overrelief='raised', command=lambda: callback(video))
            btn_exit.grid(row=0, column=1)

        def cf(window):  #
            global isBgCaptured
            new.createbg()
            isBgCaptured = 1
            window.withdraw();
            MainGame(window)
        def callback(video):
            video.destroy()
            file = open('rank', 'r')
            self.rank["text"] = "记录：" + file.read()
            file.close()
            root.update()
            root.deiconify()

        def MainGame(video):
            game = Toplevel(self.game)
            game.geometry('600x600')

            game.config(background="#F5F5F5")
            countdown = Label(game, font=("微软雅黑", 40))
            countdown.pack(pady=10)
            score=Label(game,text="准备！",font=("微软雅黑", 30))
            score.pack(pady=10)
            global scorenum
            scorenum = 2
            global randnum
            global gesture
            gesture = ""
            randnum = random.randint(0, 2)

            info = Label(game, font=("微软雅黑", 20))
            info.pack(pady=30)
            info2 = Label(game, font=("微软雅黑", 20))
            info2.pack(pady=30)
            return_btn = Button(game, text='返回', width=5, height=2, font=('微软雅黑', 14),
                                bg='#546E7A', fg='white', activebackground='#78909C',
                                relief='flat', overrelief='raised', command=lambda :close())
            return_btn.pack(pady=10)

            def count(c):
                global randnum
                countdown["text"] = "{:.1f}".format(c)
                game.config(background="#F5F5F5")
                if c > 0.1:
                    game.after(100, count, c - 0.1)
                else:
                    # c = round(random.uniform(0.5, 2.0), 1)
                    randnum = random.randint(0, 2)
                    refresh()
                    judge(gesture)
                    # game.config(bg="#ed5736")
                    # game.after(1000, count, c)

            def refresh():
                global gesture
                if (cnt == 0):
                    gesture = "石头"
                elif (cnt == 1):
                    gesture = "剪刀"
                elif (cnt == 2):
                    gesture = "布"
                else:
                    gesture = "啥？"
                info["text"] = "您出的是" + gesture
                # judge(gesture)
                # game.after(50, refresh, )

            def judge(ges):
                global scorenum

                result = cnt - randnum
                # g=""
                if randnum==0:
                    g="石头"
                elif randnum==1:
                    g="剪刀"
                else:
                    g="布"
                if result == 0:
                    info2["text"] = "电脑和您出的都是：" + ges + " 平局，筹码加10"
                    scorenum+=2
                    score["text"] = "您的筹码为：" + str(scorenum)
                elif result in (1, -2):
                    info2["text"] = "电脑出：" + g + " 您输了，失去所有筹码！"
                    scorenum=0
                    score["text"] = "您的筹码为：" + str(scorenum)
                else:
                    info2["text"] = "电脑出：" + g + " 您赢了，筹码以指数翻倍！"
                    scorenum=scorenum**2
                    score["text"] = "您的筹码为：" + str(scorenum)

                if (scorenum <= 0 ):
                    def close_win():
                        close()
                        fail.destroy()
                    fail = Toplevel(self.game)
                    fail.geometry('300x300')
                    message = Label(fail, text="很遗憾您输掉了所有赌注\n正在返回准备界面",font=('微软雅黑', 20))
                    scorenum=10
                    message.pack(pady=10)
                    game.destroy()
                    fail.after(3000,close_win)
                elif(scorenum>0):
                    def close_win():
                        with open('rank','w') as file:
                            file.write(str(scorenum))
                        file.close()
                        close()
                        fail.destroy()
                    def suoha():
                        count(1.5)
                        fail.destroy()
                    fail = Toplevel(self.game)
                    fail.geometry('300x300')
                    message = Label(fail, text="继续吗?\n您的筹码还有："+str(scorenum),font=('微软雅黑', 20))
                    message.pack(pady=10)
                    btn_continue=Button(fail,text="我就要梭哈！",command=lambda :suoha())
                    btn_continue.pack(pady=5)
                    btn_settlement=Button(fail,text="可以了，见好就收!",command=close_win)
                    btn_settlement.pack(pady=5)
                    # game.destroy()

            def close():
                global isBgCaptured
                video.deiconify() #回到准备界面
                game.destroy()
                isBgCaptured=0
                new.reset()

            count(2.5)
            game.mainloop()

    def GameQuit(self):
        root.quit()


class App():
    def __init__(self, window):
        self.window = window

        # 创建Tkinter Frame
        self.frame = Frame(self.window, width=640, height=480)
        self.frame.pack()

        # 打开摄像头
        self.cap = cap

        # 显示视频
        self.label = Label(self.frame)
        self.label.pack()
        self.show_video()

    def show_video(self):
        global cnt
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 镜像翻转图像
        frame = cv2.flip(frame, 1)
        # 添加识别范围
        cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                      (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)

        img = Image.fromarray(frame)

        if isBgCaptured == 1:  # this part wont run until background captured
            img2 = new.removeBG(frame)
            img2 = img2[0:int(cap_region_y_end * frame.shape[0]),
                   int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI
            # cv2.imshow('mask', img)

            # convert the image into binary image
            gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (new.blurValue, new.blurValue), 0)
            # cv2.imshow('blur', blur)
            ret, thresh = cv2.threshold(blur, new.threshold, 255, cv2.THRESH_BINARY)
            # cv2.imshow('ori', thresh)

            # get the coutours
            thresh1 = copy.deepcopy(thresh)
            contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            length = len(contours)
            maxArea = -1
            if length > 0:
                for i in range(length):  # find the biggest contour (according to area)
                    temp = contours[i]
                    area = cv2.contourArea(temp)
                    if area > maxArea:
                        maxArea = area
                        ci = i

                res = contours[ci]
                hull = cv2.convexHull(res)
                drawing = np.zeros(img2.shape, np.uint8)
                cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
                cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

                isFinishCal, cnt = new.calculateFingers(res, drawing)
                if cnt > 2:
                    cnt = 2
                # print(cnt)

        if not hasattr(self, 'imgtk'):
            self.imgtk = ImageTk.PhotoImage(image=img)
        else:
            self.imgtk.paste(img)

        # 将图像显示在Tkinter Frame中
        self.label.config(image=self.imgtk)

        # 循环更新视频
        self.window.after(1, self.show_video)


Game()  # 实例化
