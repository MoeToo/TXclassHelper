#!/usr/bin/env python
# -*- coding:utf-8 -*-

# --------------------------------------------------------
# 疼讯课堂小助手 (TXClass Helper) Ver 0.6
# Copyright (c) 2022 MoeTwo Studio
# Licensed under The MIT License
# Written by Coolsong
# 提示：在运行本程序前请先阅读自述文件。
# Tip: Please read the readme file before running this.
# --------------------------------------------------------
import base64  # 引入编码库
import threading  # 开线程
from time import sleep
import os
import cv2
import pyautogui
import pyscreeze
import datetime
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
import tkinter.messagebox
import winsound


class Application_ui(Frame):
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('疼讯课堂小助手 v0.6')
        self.master.geometry('350x400')
        self.master.resizable(0, 0)  # 禁止拉伸
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()
        self.style = Style()
        self.style.configure('TCommand.TButton', font=('微软雅黑', 9))
        self.TextFont = Font(font=('微软雅黑', 9))

        self.Command1 = Button(self.top, text='开始运行', command=self.Command1_Cmd, style='TCommand.TButton')
        self.Command1.place(x=10, y=10, width=70, height=30)

        self.Command2 = Button(self.top, text='清空日志', command=self.Command2_Cmd, style='TCommand.TButton')
        self.Command2.place(x=100, y=10, width=70, height=30)

        self.Label = Label(self.top, text="使用场景", font=self.TextFont)
        self.Label.place(x=190, y=15)

        v = IntVar()
        v.set(0)
        self.Command3 = Radiobutton(self.top, text='客户端', variable=v, value=0, command=self.Command3_Cmd)
        self.Command3.place(x=190, y=45)
        self.Command4 = Radiobutton(self.top, text='网页版', variable=v, value=1, command=self.Command4_Cmd)
        self.Command4.place(x=260, y=45)

        self.Command5 = Button(self.top, text='查看截图', command=self.Command5_Cmd, style='TCommand.TButton')
        self.Command5.place(x=10, y=50, width=160, height=30)

        self.sep1 = Separator(self.top, orient=HORIZONTAL)
        self.sep1.pack(padx=10, pady=95, fill='x')

        self.Label = Label(self.top, text="运行日志", font=self.TextFont)
        self.Label.place(x=10, y=115)

        self.Text = Text(self.top, fg='#bbbbbb', bg='#3c3f41', font=self.TextFont)
        self.Text.place(x=10, y=140, width=330, height=250)


class Application(Application_ui):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def clickCheck(self):
        time = datetime.datetime.now().strftime('%H时%M分%S秒')
        try:
            self.Text.insert('1.0', f"{time}-监测进程已启动\n")
            winsound.Beep(600, 500)
            while 1:
                # 先截图
                screenshot = pyscreeze.screenshot('temp_screenshot.png')
                # 读取图片 灰色会快
                temp = cv2.imread(r'temp_screenshot.png', cv2.IMREAD_GRAYSCALE)

                theight, twidth = target.shape[:2]
                tempheight, tempwidth = temp.shape[:2]
                # print("目标图宽高：" + str(twidth) + "-" + str(theight))
                # print("模板图宽高：" + str(tempwidth) + "-" + str(tempheight))
                # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
                scaleTemp = cv2.resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
                stempheight, stempwidth = scaleTemp.shape[:2]
                # print("缩放后模板图宽高：" + str(stempwidth) + "-" + str(stempheight))
                # 匹配图片
                res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
                mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val >= 0.9:
                    time = datetime.datetime.now().strftime('%H时%M分%S秒')

                    # 计算出中心点
                    top_left = max_loc
                    bottom_right = (top_left[0] + twidth, top_left[1] + theight)
                    tagHalfW = int(twidth / 2)
                    tagHalfH = int(theight / 2)
                    tagCenterX = top_left[0] + tagHalfW
                    tagCenterY = top_left[1] + tagHalfH
                    # 左键点击屏幕上的这个位置
                    pyautogui.click(tagCenterX, tagCenterY, button='left')

                    self.Text.insert('1.0', f"{time}-发现签到，已尝试点击并于1秒后对结果进行截图\n")
                    winsound.Beep(1000, 1000)
                    sleep(1)
                    screenshot = pyscreeze.screenshot(f'result/{time}.png')
                sleep(5)
        except Exception as err:
            time = datetime.datetime.now().strftime('%H时%M分%S秒')
            self.Text.insert('1.0', f"{time}-ERROR！错误信息：\n{err}\n")
            self.Command1['text'] = '发生错误'
            winsound.Beep(600, 1000)
            tkinter.messagebox.showerror('错误', f'监测进程发生错误，请尝试重新运行程序！\n时间：{time}')

    def command1(self):
        global screenScale, target
        # 屏幕缩放系数 mac缩放是2 windows一般是1
        screenScale = 1

        # 事先读取按钮截图
        if button_img == '':
            tkinter.messagebox.showinfo('提示', '请先选择使用场景')

        else:
            target = cv2.imread(rf"{button_img}", cv2.IMREAD_GRAYSCALE)
            if not os.path.exists("result/"):  # 新建文件夹
                os.mkdir("result/")

            time = datetime.datetime.now().strftime('%H时%M分%S秒')
            self.Command1.configure(state=DISABLED)
            self.Command3.configure(state=DISABLED)
            self.Command4.configure(state=DISABLED)
            self.Command1['text'] = '正在运行'
            self.Text.insert('1.0', f"{time}-开始运行\n=====\n提示：请以管理员身份运行本程序\n否则有可能无法执行点击操作\n操作方法：右键点击本程序选择'以管理员身份运行'\n"
                                    f"=====\n")
            self.clickCheck()
            pass

    def command2(self):
        self.Text.delete("1.0", END)

    def Command1_Cmd(self, event=None):
        self.thread_it(self.command1)

    def Command2_Cmd(self, event=None):
        self.thread_it(self.command2)

    def Command3_Cmd(self, event=None):
        global button_img
        button_img = 'pc.png'
        time = datetime.datetime.now().strftime('%H时%M分%S秒')
        self.Text.insert('1.0', f"{time}-使用场景已设置为：客户端\n")

    def Command4_Cmd(self, event=None):
        global button_img
        button_img = 'web.png'
        time = datetime.datetime.now().strftime('%H时%M分%S秒')
        self.Text.insert('1.0', f"{time}-使用场景已设置为：网页端\n")

    def Command5_Cmd(self, event=None):
        if not os.path.exists("result/"):
            time = datetime.datetime.now().strftime('%H时%M分%S秒')
            self.Text.insert('1.0', f"{time}-提示：你还没有运行截图，请先运行再试！\n")
        else:
            os.startfile("result")

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)  # 守护--就算主界面关闭，线程也会留守后台运行（不对!）
        t.start()  # 启动
        # t.join()          # 阻塞--会卡死界面！


if __name__ == "__main__":
    button_img = ''
    img = '''AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/31nLv99Zy4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/gIAC/4JmZP+BZ+X/gWfl/4JmZP+AgAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/gGgc/oBml/+Faev/gWj9/4Fn/f+Fauv+gGaX/4BmGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP+AAAL/hGMY/35osf+Kbe//fmrn/4lgkf+JYJH/fmrn/4hs7/+AZrv/gGU+AAAAAAAAAAAAAAAAAAAAAAAAAAD/uToG/8Q0dv+QWpX/gm61/plUkf/FOLn/xDe5/5pTjf6Ba8X/hmz3/oBlsf+qqgIAAAAAAAAAAAAAAAAAAAAA/79ABv/JMsH/wzfF/7RDn//FNcv/zjPx/80y8f/JNcn/rUiZ/4Zpsf99Z8f+hoYEAAAAAAAAAAAAAAAAAAAAAP+/QAL/yTPR/88z9//PM9v/yjP7/8o0///JL///yzP7/88z0f+4Qav/jluD/4CAAgAAAAAAAAAAAAAAAP+qVQL/yTM8/8oz4//MM///zDP//8kz///cfP//0E7//8ct///MMv//zzPj/8Q3qf/LNDz/qlUCAAAAAP/LNBr+yDNU/8w0tf/LM/n/yTP//8kz///IMv//8cv//+qw///UYP//yTX//8sz///MMvf+zjSz/8gzVv/HMxr/yDJU/8kzz//PNf//yjP//8kz///JM///yDH///Xc/////v//7b3//81E///IL///yjP//881///JM9H/yDJU/8cyVv/KM7n/zTTt/8sz///JM///yTP//8gx///12///+Of//+qw///NRv//yDD//8sz///NNO3/yjO5/8kyVgAAAAD/yzMo/8o0mf/PNOH/yjP//8oz///IMv//7b3//+KT///KOv//yC7//8o0///PNOH/yjSZ/8YyKAAAAAAAAAAAAAAAAP/INwz/yzNw/8sz2f/NNPn/yjT//9JW///IL///yTD//800+f/LM9v/yzNw/8g3DAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/KMkL/yzPD/9A08//ILf//yTP//9A08//LM8P/xzFEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/78uGv7JNJ3/zDT3/8w09/7LNJ3/yC4aAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/8k0if/LNIkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//8AAP5/AAD4HwAA8A8AAPAHAADgBwAA4AcAAOAHAADAAwAAgAEAAIABAADAAwAA8A8AAPgfAAD8PwAA/n8AAA== '''
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    top = Tk()
    top.iconbitmap('tmp.ico')
    os.remove("tmp.ico")  # 删掉临时文件
    Application(top).mainloop()
