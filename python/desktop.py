# -*- coding: utf-8 -*-
# pip install python-qt5

import serial
import sys
import time
import win32gui
from img2hex import img2hex as i2h

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageQt

i2h = i2h()

ser = serial.Serial()

rgb_size = (28, 16)

app = QApplication(sys.argv)
screen = QApplication.primaryScreen()


def port_open():
    ser.port = "COM1"  # 设置端口号
    ser.baudrate = 9600  # 设置波特率
    ser.bytesize = 8  # 设置数据位
    ser.stopbits = 1  # 设置停止位
    ser.parity = "N"  # 设置校验位
    ser.open()  # 打开串口,要找到对的串口号才会成功
    if (ser.isOpen()):
        print("打开成功")
    else:
        print("打开失败")


def port_close():
    ser.close()
    if (ser.isOpen()):
        print("关闭失败")
    else:
        print("关闭成功")


def send(send_data):
    if (ser.isOpen()):
        ser.write(send_data)  # Hex发送
    else:
        print("发送失败")


def get_frame():
    qtimg = screen.grabWindow(0).toImage()
    image = ImageQt.fromqimage(qtimg)
    im = image.resize(rgb_size)
    # im.save("img/"+str(time.time())+".jpg")
    ima = im.load()
    hex = []
    for ly in range(rgb_size[1]):
        for pix in ima[0, 15 - ly]:
            hex.append(pix)

    for x in range(rgb_size[0]):
        for pix in ima[x, 0]:
            hex.append(pix)

    for ry in range(rgb_size[1]):
        for pix in ima[rgb_size[0] - 1, ry]:
            hex.append(pix)
    return hex
    # print(hex)


if __name__ == '__main__':
    port_open()
    while True:
        hex = get_frame()
        send(hex)
        exit()
