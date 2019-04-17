# coding:utf8
from configure import configuration
import pprint
from icon import img, flash
import base64
import winreg
import win32con
import win32clipboard as wc
from tkinter import *
from tkinter import filedialog, ttk, PhotoImage
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image, ImageTk
import time
import imageio

import threading


#!python3
import win32gui
import time
from win32con import PAGE_READWRITE, MEM_COMMIT, MEM_RESERVE, MEM_RELEASE, PROCESS_ALL_ACCESS, WM_GETTEXTLENGTH, WM_GETTEXT
from commctrl import LVM_GETITEMTEXT, LVM_GETITEMCOUNT, LVM_GETNEXTITEM, LVNI_SELECTED
import os
import struct
import ctypes
import win32api
import shutil
import io

from pynput import keyboard

Quit = False
Esc = False
idx = 0
total_dict = {}
bg_color = 'white'


def on_press(key):
    try:
        print(f'字母 {key.char} 被按下了')
    except AttributeError:
        print(f'特殊的键 {key} 被按下了')
    plt.close()


def on_release(key):
    global total_dict, idx, Quit, Esc
    dict = {'1': '清晰的车牌', }

    if key == keyboard.Key.esc:
        try:
            idx -= 1
            Esc = True
            shutil.move(
                os.path.join(
                    present_dir + '_classify',
                    total_dict[idx],
                    str(idx) + '.jpg'),
                os.path.join(present_dir))

        except BaseException:
            win32api.MessageBox(win32con.NULL, '你已经回退到了最开始', '警告！',
                                win32con.MB_OK)
            return False

    elif str(key)[1:-1] in ['1', '2', '3', '4', '5']:
        shutil.move(
            os.path.join(
                present_dir,
                str(idx) +
                '.jpg'),
            os.path.join(
                present_dir +
                '_classify',
                str(key)[
                    1:-
                    1]))
        total_dict[idx] = str(key)[1:-1]
        return False
    elif str(key)[1:-1] == 'q':
        Quit = True
        return False

    return True


root = Tk(className='分类数据标注工具_V1_20180927')
root.geometry('800x550')
# root.state("zoomed")
root.config(bg=bg_color)
# root.attributes("-fullscreen", True)
# sss

# 将import进来的icon.py里的数据转换成临时文件tmp.ico，作为图标
tmp = open("tmp.ico", "wb+")
tmp.write(base64.b64decode(img))
tmp.close()

# tmp = open("flash.jpg", "wb+")
# tmp.write(base64.b64decode(flash))
# tmp.close()

root.iconbitmap('tmp.ico')  # 加图标
os.remove("tmp.ico")
# 以上是为exe制作icon


# root.iconbitmap('logo48.ico')


class Decorate(object):
    def __init__(self):
        self.video = 'con3.mp4'

    def showflash(self):
        image1 = "flash.gif"
        # 初始坐标
        x0 = 50.0
        y0 = 50.0
        # 列表将包含所有的x和y坐标.到目前为止，他们只包含初始坐标
        x = [x0]
        y = [y0]
        # 每次移动的速度或距离
        vx = 10.0  # x 速度
        vy = 5  # y 速度
        # 边界，这里要考虑到图片的大小，要预留一半的长和宽
        x_min = 46.0
        y_min = 46.0
        x_max = 754.0
        y_max = 554.0
        # 图片间隔时间,要动画效果，此处设为每秒４０帧
        sleep_time = 0.025
        # 运行步数
        range_min = 1
        range_max = 200
        # 创建500次的x和y坐标
        for t in range(range_min, range_max):
            # 新坐标等于旧坐标加每次移动的距离

            new_x = x[t - 1] + vx
            new_y = y[t - 1] + vy
        # 如果已经越过边界，反转方向
            if new_x >= x_max or new_x <= x_min:
                vx = vx * -1.0
            if new_y >= y_max or new_y <= y_min:
                vy = vy * -1.0
                # 添加新的值到列表
            x.append(new_x)
            y.append(new_y)

    # 开始使用ｔｋ绘图

        canvas = Canvas(width=80, height=200, bg='white')
        canvas.pack()
        photo1 = PhotoImage(file=image1)
        width1 = photo1.width()
        height1 = photo1.height()
        image_x = (width1) / 2.0
        image_y = (height1) / 2.0

        # 每次的移动
        for t in range(range_min, range_max):
            canvas.create_image(x[t], y[t], image=photo1, tag="pic")
            canvas.update()

            # 暂停0.05妙，然后删除图像
            time.sleep(sleep_time)
            canvas.delete("pic")

    def stream(self, label):
        imageio.plugins.ffmpeg.download()
        video_name = self.video  # This is your video file path
        video = imageio.get_reader(video_name)
        frame = 0
        for image in video.iter_data():
            frame += 1  # counter to save new frame number
            image_frame = Image.fromarray(image)
            # image_frame.save('FRAMES/frame_%d.png' % frame)  # if you need
            # the frame you can save each frame to hd
            frame_image = ImageTk.PhotoImage(image_frame)
            label.config(image=frame_image)
            label.image = frame_image
            if frame == 1400:
                break  # after 40 frames stop, or remove this line for the entire video

    def showvideo(self):

        my_label = Label(
            window,
            width=400,
            height=500,
            bg='red',
            fg='yellow',
            font='Times 30 bold',
            wraplength=800,
            anchor='n')
        my_label.pack()
        thread = threading.Thread(target=self.stream, args=(my_label,))
        thread.daemon = 1
        thread.start()


def clearClipboard():
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.CloseClipboard()


def getTextFromClipboard():
    wc.OpenClipboard()
    d = wc.GetClipboardData(win32con.CF_TEXT)
    wc.CloseClipboard()
    return d


def show_tips():
    win32api.MessageBox(
        win32con.NULL, '    1, 这是一份简短的说明,只在第一次打开软件时自动显示，以后如果想要查看请点击“查看说明”按钮'
        ' \n    2, 选择合适的目录，选择是否重命名（图片名称要求为“有序数字.jpg”，例如，"1.jpg、2.jpg"等等）。'
        '点击开始处理，按键F1-F5可以将当前图片自动移动到上一级目录下文件名为“当前文件夹名+classify”'
        '下的5个次级目录内。'
        '\n    3, 按键ESC是回退键，可以使你还原上一张错分类的图片，但是要注意，不可以回退到开始之前（否则会卡bug要求重启软件）'
        '\n    4, 按键 Q 有助于退出处理界面、关闭之前建议敲一下Q'
        '\n    5, 其他按键无效'
        '\n\n PS.不要乱按键会卡BUG', '你好，操作员', win32con.MB_OK)


config = configuration
if config['Opening_tips'] == 'yes':
    show_tips()
    config['Opening_tips'] = 'no'

present_dir = config['deal_list'][0]


def cv_video():
    def resize(image):
        im = image
        new_siz = siz
        im.thumbnail(new_siz, Image.ANTIALIAS)
        return im

    def size(event):
        global siz
        if siz == screenWH:
            siz = (200, 200)
        else:
            siz = screenWH
            win.state('zoomed')
        print('size is: ', siz)

    def view_frame_video():
        vc = cv2.VideoCapture('con4.mp4')
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            rval = False

        while rval:
            rval, frame, = vc.read()
            print(frame)
            img = Image.fromarray(frame)
            img = resize(img)
            imgtk = ImageTk.PhotoImage(img)
            lbl.config(image=imgtk)
            lbl.img = imgtk
            cv2.waitKey(1)

        vc.release()
        t = threading.Thread(target=view_frame_video)
        t.start()

    win = Toplevel()

    screenWH = (win.winfo_screenwidth(), win.winfo_screenheight())
    siz = (200, 200)

    frm_ = Frame(bg='black')
    frm_.pack()
    lbl = Label(frm_, bg='black')
    lbl.pack(expand=True)
    lbl.bind('<Double-Button-1>', size)
    view_frame_video()
    frm = Frame()
    frm.pack()

    win.mainloop()


def cv_video2():
    def resize(image):
        im = image
        new_siz = siz
        im.thumbnail(new_siz, Image.ANTIALIAS)
        return im

    def size(event):
        global siz
        if siz == screenWH:
            siz = (600, 600)
        else:
            siz = screenWH
            win.state('zoomed')
        print('size is: ', siz)

    def view_frame_video():
        vc = cv2.VideoCapture('con4.mp4')
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            rval = False

        while rval:
            rval, frame = vc.read()
            img = Image.fromarray(frame)
            img = resize(img)
            imgtk = ImageTk.PhotoImage(img)
            lbl.config(image=imgtk)
            lbl.img = imgtk
            if stop:
                vc.release()
                break  # stop the loop thus stops updating the label and reading imagge frames
            cv2.waitKey(1)
        vc.release()

    def stop_():
        global stop
        stop = True

    def play():
        stop = False
        t = threading.Thread(target=view_frame_video)
        t.start()

    # root = Tk()
    win = Toplevel()

    stop = None
    screenWH = (win.winfo_screenwidth(), win.winfo_screenheight())
    siz = (1920, 1080)

    # Label(text='Press Play Button').pack()
    frm_ = Frame(win, bg='black')
    frm_.pack()
    lbl = Label(frm_, bg='black')
    lbl.pack(expand=True)
    # lbl.bind('<Double-Button-1>', size)

    frm = Frame()
    frm.pack()
    Button(win, text='Play', command=play).pack(side=LEFT)
    Button(win, text='Stop', command=stop_).pack(side=LEFT)

    # root.mainloop()


def video():
    try:
        imageio.plugins.ffmpeg.download()
        video_name = 'con3.mp4'  # This is your video file path
        video = imageio.get_reader(video_name)

        def stream():
            window = Toplevel()
            window.title('你好坏坏')
            video_player = Label(window, height=300, width=400)

            frame = 0
            for image in video.iter_data():
                frame += 1  # counter to save new frame number
                print(frame)
                image_frame = Image.fromarray(image)
                # image_frame.save('FRAMES/frame_%d.png' % frame)  # if you
                # need the frame you can save each frame to hd
                frame_image = ImageTk.PhotoImage(image_frame)
                video_player.config(image=frame_image)
                video_player.image = frame_image
                # video_player.config(text='sssss')
                time.sleep(0.1)

                if frame == 1400:
                    break
            video_player.pack()
            window.destroy()

        thread = threading.Thread(target=stream, args=())
        thread.daemon = 1
        thread.start()

        # frame = 0
        # for image in video.iter_data():
        #     frame += 1  # counter to save new frame number
        #     image_frame = Image.fromarray(image)
        #     # image_frame.save('FRAMES/frame_%d.png' % frame)  # if you need the frame you can save each frame to hd
        #     frame_image = ImageTk.PhotoImage(image_frame)
        #     video_player.config(image=frame_image)
        #     video_player.image = frame_image
        #     # video_player.config(text='sssss')
        #     time.sleep(0.1)
        #
        #     if frame == 1400:
        #         break

    except Exception as e:
        print(e)
        win32api.MessageBox(
            win32con.NULL,
            '恭喜，你已处理完这个文件夹！',
            '恭喜',
            win32con.MB_OK)


decoration = Decorate()
# decoration.showflash()
# cv_video2()


# key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Explorer")
# try:
#     i = 0
#     while 1:
#         name = winreg.EnumKey(key, i)
#         print(str(name))
#         i += 1
# except WindowsError:
#     print('end')


def re_name():
    global present_dir
    allfiles = os.listdir(present_dir)
    for each in allfiles:
        os.rename(
            os.path.join(
                present_dir, each), os.path.join(
                present_dir, each + '_tmp' + '.jpg'))

    allfiles = os.listdir(present_dir)
    index = 0
    for each in allfiles:
        os.rename(
            os.path.join(
                present_dir, each), os.path.join(
                present_dir, str(index) + '.jpg'))
        index += 1


def choose():
    global present_dir

    # Tk().withdraw() # Close the root window
    in_path = filedialog.askdirectory()

    if in_path not in config['deal_list']:

        signal = win32api.MessageBox(
            win32con.NULL, '%s\n这个路径以前并没有处理过，请进行点击“是”按钮进行重命名操作，'
            '若如此做，将会将该路劲下的所有文件进行重命名（请保证该文件夹下没有其他的子文件夹）,'
            '该重命名操作不可恢复，请保证它是以前没有进行过处理的文件夹。\n'
            '反之，如果这是您移动文件夹位置导致的路径变更，请点击“否”，将不用进行重命名操作，'
            '可以直接开始处理，但是请选择正确的用于保存的文件夹\n'
            '点击取消可以重新选择' %
            (in_path), '重要提示！', win32con.MB_YESNOCANCEL)
        # 是：6, 否：7, 取消:2
        if signal == 6:
            present_dir = in_path
            re_name()
            config['deal_list'].insert(0, in_path)
            print(config['deal_list'])

        elif signal == 7:
            config['deal_list'].insert(0, in_path)
            present_dir = in_path
    else:
        present_dir = in_path
        config['deal_list'].remove(in_path)
        config['deal_list'].insert(0, in_path)


def cv_imread(file_path):
    try:
        cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        return cv_img
    except BaseException:
        win32api.MessageBox(
            win32con.NULL,
            '读取目录下图片出错，请确保目录下只有jpg图片并重启软件！',
            '错误提示！',
            win32con.MB_OK)
    return None


def classify():
    global idx, Quit, Esc
    Quit = False
    if not os.path.isdir(present_dir):
        T1.config(text='%s\n您还没有选择工作目录，请重新选择' % (present_dir))
    else:
        T0.config(text='现在处理的文件夹是：')
        T1.config(text=present_dir)
    allfiles = os.listdir(present_dir)
    if len(allfiles) == 0:
        win32api.MessageBox(
            win32con.NULL,
            '读取目录下图片出错，请确保目录下存在有jpg图片并重启软件！',
            '错误提示！',
            win32con.MB_OK)
        return
    for each in allfiles:
        if each[-3:] != 'jpg':
            win32api.MessageBox(
                win32con.NULL,
                '请务必保证处理的文件夹下所有文件都是jpg格式',
                '错误提示！',
                win32con.MB_OK)
            return

    result_dir = present_dir + '_classify'
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    class_list = []
    for index in range(5):
        tmp_dir = result_dir + '/' + str(index + 1)
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        class_list.append(tmp_dir)

    allfiles.sort(key=lambda x: int(x[:-4]))
    min_index = int(allfiles[0][:-4])
    max_index = int(allfiles[-1][:-4])
    idx = min_index
    while(idx <= max_index):

        image_now = present_dir + '/' + str(idx) + '.jpg'
        # print(image_now)
        img = cv_imread(image_now)
        # img = mpimg.imread(image_now)
        # img = Image.open(image_now)
        # with open(image_now, 'rb') as f:
        #     img = Image.open(io.BytesIO(f.read()))
        try:
            print('idx_show:', idx)
            cv2.imshow('Click End Key to quit -- No.%d' % (idx), img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # plt.imshow(img)
            # plt.axis('off')
            # plt.show()
            # img.show()

        except BaseException:
            win32api.MessageBox(win32con.NULL, '产生了某个关于图片显示的未知错误', '错误提示！',
                                win32con.MB_OK)
        T2.config(text='注意，退出处理不要点叉叉，要按 Q 键，否则会卡BUG！')
        with keyboard.Listener(
                on_release=on_release) as listener:
            listener.join()
        # if Esc is not True:
        #     idx += 1
        # Esc = False
        idx += 1
        if Quit:
            return
    if idx > max_index:
        win32api.MessageBox(
            win32con.NULL,
            '你成功处理完成了该文件夹下的所有文件',
            '恭喜！Level-Up！',
            win32con.MB_OK)
    return


# T1 = Text(root, height=10, width=80)

title = Canvas(root, bg=bg_color, height=200, width=690)

image_file = ImageTk.PhotoImage(file='welcome6.jpeg')
image = title.create_image(0, -40, anchor=NW, image=image_file)
title.scale(image, 0, 0, 2, 5)
# print(title.winfo_width(), title.winfo_height())
title.pack(side=TOP)


# image_bg = PhotoImage(file='welcome.gif')
# background = Label(root, text='', image=image_bg, compound=CENTER, font=("华文行楷",20))
# background.pack()
# contain = Canvas(root, height=200, width=500)
image_contain = PhotoImage(file='xiamu.gif')
# contain.create_image(0,0, anchor=NW, image=image_contain)
# contain.pack(side=BOTTOM)


frame = Frame(root, bg=bg_color)
frame.pack()

image_t1 = PhotoImage(file='xiamu.gif')
T0 = Label(
    frame,
    width=40,
    height=2,
    bg=bg_color,
    fg='black',
    font='华文行楷 15 bold',
    wraplength=800,
    anchor='center',
    justify='left',
    padx=10)
T0.config(text='当前默认工作目录是上次打开的目录：')

T1 = Label(
    frame,
    text="同志们辛苦了！!",
    width=60,
    height=2,
    bg=bg_color,
    fg='black',
    font='楷书 13 bold',
    wraplength=800,
    anchor='center',
    justify='left',
    padx=10)
# T1 = Message(frame)
T1.config(text=present_dir)

T2 = Label(
    frame,
    text="注意，退出处理不要点叉叉，要按 Q 键，否则会BUG！",
    width=60,
    height=5,
    bg=bg_color,
    fg='red',
    font='Times 10 bold',
    wraplength=800,
    anchor='n')


T0.grid(row=1, column=1, padx=0, pady=0)
T1.grid(row=2, column=1, padx=0, pady=0)
T2.grid(row=3, column=1, padx=0, pady=0)


keys = Frame(root, bg=bg_color)
keys.pack(side=BOTTOM)

key_A = Button(
    keys,
    bg='light blue',
    relief=RAISED,
    width=15,
    height=1,
    text='选择操作文件夹',
    command=choose)
key_B = Button(
    keys,
    bg='light blue',
    relief=RAISED,
    width=15,
    height=1,
    text='查看说明',
    command=show_tips)
key_C = Button(
    keys,
    highlightcolor='blue',
    bg='light yellow',
    relief=RAISED,
    fg='black',
    width=15,
    height=1,
    text='开始处理',
    font=(
        '华文楷体',
        20),
    command=classify,
    activeforeground='black',
    activebackground='cyan')
key_D = Button(
    keys,
    bg='light blue',
    relief=RAISED,
    width=15,
    height=1,
    text='重命名（慎点）',
    command=re_name)

key_D.grid(row=2, column=1, padx=20, pady=20)
key_B.grid(row=2, column=2, padx=20, pady=20)
key_C.grid(row=1, column=2, padx=20, pady=20, ipadx=0, ipady=0)
key_A.grid(row=2, column=3, padx=20, pady=20)

root.mainloop()

# input('aaa')

print('config:', config)
with open('configure.py', 'w', encoding='utf-8') as fid:
    fid.write('configuration = ' + str(config))


# ==============================================================
