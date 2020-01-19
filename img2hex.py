# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageFilter
import math


class img2hex:
    # 初始化
    def __init__(self):
        pass

    def tohex(self, im):
        size = 128, 64  # 屏幕大小
        mode = 0  # 模式及过滤选择：0：纯灰度、 1：边缘提取、 2:模糊、 3:轮廓 4:边缘增强 5:浮雕 6:锐化 7:光滑
        invert = 0  # 像素颜色反选
        threshold = 0  # 二值化阈值 0-255，单色屏幕中灰度大于此阈值的则被显示

        show_wh = 1  # 显示宽高
        show_pixel = 1  # 二进制图像打印显示

        im.thumbnail(size)
        if (mode == 1):
            ipx = im.convert('L').filter(ImageFilter.FIND_EDGES)
        elif (mode == 2):
            ipx = im.convert('L').filter(ImageFilter.BLUR)
        elif (mode == 3):
            ipx = im.convert('L').filter(ImageFilter.CONTOUR)
        elif (mode == 4):
            ipx = im.convert('L').filter(ImageFilter.EDGE_ENHANCE)
        elif (mode == 5):
            ipx = im.convert('L').filter(ImageFilter.EMBOSS)
        elif (mode == 6):
            ipx = im.convert('L').filter(ImageFilter.SHARPEN)
        elif (mode == 7):
            ipx = im.convert('L').filter(ImageFilter.SMOOTH)
        else:
            ipx = im.convert('L')
        w, h = ipx.size
        if (show_wh == 1):
            print(w, h)

        ima = ipx.load()

        row = []
        col = []
        hex_arr = []
        hexStr = ""
        cnt_MaxNum = math.ceil(w / 8)
        hexRowStr = ""
        for x in range(h):
            if (row != []):
                for z in row:
                    hexStr = str(hexStr + str(z))
                    hexRowStr = str(hexRowStr + str(z))
                    if (len(hexStr) == w and w % 8 != 0 and Img_MakeUp == 1):
                        for x in range(8 * cnt_MaxNum - w):
                            hexStr = str(hexStr + str(0))
                    if (len(hexRowStr) == w and len(hexRowStr) % 8 != 0):
                        for y in range(len(hexRowStr) % 8):
                            hexStr = str(hexStr + str(0))
                    if (len(hexStr) == 8):
                        col.append(hexStr)
                        hexStr = hexStr[::-1]
                        xbb = str(int(hexStr, 2))
                        hex_arr.append(xbb)
                        hexStr = ""
            if (show_pixel == 1):
                print(hexRowStr)
            
            hexStr = ""
            hexRowStr = ""
            row = []
            for y in range(w):
                if (invert == 0):
                    if (ima[y, x] > threshold):
                        row.append(1)
                    else:
                        row.append(0)
                if (invert == 1):
                    if (ima[y, x] > threshold):
                        row.append(0)
                    else:
                        row.append(1)

        
        return hex_arr
