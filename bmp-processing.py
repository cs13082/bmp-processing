""" This program converts ./gazou1.bmp to ./gazou2.bmp """
# -*- coding: UTF-8 -*-
# Tested on Python 3.6.3 (32bit)

READPATH = r"./gazou1.bmp"
WRITEPATH = r"./gazou2.bmp"

class BmpFile:
    """
    BMP file Header
    2byte bm 識別文字（BM）
    4byte filesize ファイルサイズ
    2byte res_a 予約領域（0）
    2byte res_b 予約領域（0）
    4byte headersize ヘッダサイズ
    4byte infosize 情報サイズ（40）
    4byte width 横サイズ width
    4byte height 縦サイズ height
    2byte pixnum 画数（1）
    2byte colordepth 色ビット数
    4byte compmethod 圧縮方式
    4byte compsize 圧縮サイズ
    4byte horizonalres 水平解像度
    4byte Verticalres 垂直解像度
    4byte colornum 色数
    4byte impcolornum 重要色数
    """
    def __init__(self):
        self.__idchara = bytes()
        self.__filesize = bytes()
        self.__res_a = bytes()
        self.__res_b = bytes()
        self.__headersize = bytes()
        self.__infosize = bytes()
        self.__width = bytes()
        self.__height = bytes()
        self.__pixnum = bytes()
        self.__colordepth = bytes()
        self.__compmethod = bytes()
        self.__compsize = bytes()
        self.__horizonalres = bytes()
        self.__verticalres = bytes()
        self.__colornum = bytes()
        self.__impcolornum = bytes()
        self.__color_r = []
        self.__color_g = []
        self.__color_b = []

    def read(self, bmpfile):
        self.__idchara = bmpfile.read(2)
        self.__filesize = bmpfile.read(4)
        self.__res_a = bmpfile.read(2)
        self.__res_b = bmpfile.read(2)
        self.__headersize = bmpfile.read(4)
        self.__infosize = bmpfile.read(4)
        self.__width = bmpfile.read(4)
        self.__height = bmpfile.read(4)
        self.__pixnum = bmpfile.read(2)
        self.__colordepth = bmpfile.read(2)
        self.__compmethod = bmpfile.read(4)
        self.__compsize = bmpfile.read(4)
        self.__horizonalres = bmpfile.read(4)
        self.__verticalres = bmpfile.read(4)
        self.__colornum = bmpfile.read(4)
        self.__impcolornum = bmpfile.read(4)

        tmp = 0
        while 1:
            readtmp = bmpfile.read(1)
            # ファイル終了時break
            if readtmp == b'':
                break
            readtmpint = int.from_bytes(readtmp, 'little')
            if tmp == 0:
                self.__color_b.append(readtmpint)
                tmp += 1
            elif tmp == 1:
                self.__color_g.append(readtmpint)
                tmp += 1
            elif tmp == 2:
                self.__color_r.append(readtmpint)
                tmp = 0

    def write(self, filepath):
        try:
            bmpdata = open(filepath, 'wb')
            bmpdata.write(self.__idchara)
            bmpdata.write(self.__filesize)
            bmpdata.write(self.__res_a)
            bmpdata.write(self.__res_b)
            bmpdata.write(self.__headersize)
            bmpdata.write(self.__infosize)
            bmpdata.write(self.__width)
            bmpdata.write(self.__height)
            bmpdata.write(self.__pixnum)
            bmpdata.write(self.__colordepth)
            bmpdata.write(self.__compmethod)
            bmpdata.write(self.__compsize)
            bmpdata.write(self.__horizonalres)
            bmpdata.write(self.__verticalres)
            bmpdata.write(self.__colornum)
            bmpdata.write(self.__impcolornum)

            for i in range(len(self.__color_b)):
                bmpdata.write(self.__color_b[i].to_bytes(1, 'little'))
                bmpdata.write(self.__color_g[i].to_bytes(1, 'little'))
                bmpdata.write(self.__color_r[i].to_bytes(1, 'little'))

            bmpdata.close()
        except():
            print("OPEN ERROR")
            exit()

    def getwidth(self):
        """ Returns width by int """
        return int.from_bytes(self.__width, 'little')

    def getheight(self):
        """ Returns height by int """
        return int.from_bytes(self.__height, 'little')

    def getBGR(self):
        """ Returns arr[width][height][color(gbr)] """
        arr = [[0 for i in range(self.getheight())] for j in range(self.getwidth())]
        for i in range(len(self.__color_b)):
            arr[i%self.getwidth()][i//self.getwidth()] = [self.__color_b[i], self.__color_g[i], self.__color_r[i]]
        return arr

    def setBGR(self, arr):
        """ requires gbr array """
        i = 0
        for hei in range(self.getheight()):
            for wid in range(self.getwidth()):
                self.__color_b[i] = arr[wid][hei][0]
                self.__color_g[i] = arr[wid][hei][1]
                self.__color_r[i] = arr[wid][hei][2]
                i += 1

def main():
    print("\nConvert {} to {}".format(READPATH, WRITEPATH))
    print("1 - Greyscale (Middle value)")
    print("2 - Greyscale (NTSC Coef. method)")
    print("3 - Color Inversion")
    print("4 - Blur")
    keyinput = input("\nPlease type the number: ")

    bmpdata = BmpFile()

    # readBMP
    bmpdata.read(open(READPATH, 'rb'))
    print("Read the file")

    # Image Processing
    if int(keyinput) == 1:
        convertToGreyscale1(bmpdata)
    elif int(keyinput) == 2:
        convertToGreyscale2(bmpdata)
    elif int(keyinput) == 3:
        invertColors(bmpdata)
    elif int(keyinput) == 4:
        blurImage(bmpdata)

    # writeBMP
    bmpdata.write(WRITEPATH)
    print("Wrote the file")


def convertToGreyscale1(bmpdata):
    """ middle value """
    arr = bmpdata.getBGR()
    for hei in range(bmpdata.getheight()):
        for wid in range(bmpdata.getwidth()):
            calc = (max(arr[wid][hei]) + min(arr[wid][hei])) // 2
            arr[wid][hei] = [calc, calc, calc]
    bmpdata.setBGR(arr)
    print("Greyscaled (Middle value) the file")

def convertToGreyscale2(bmpdata):
    """ NTSC Coef. method """
    arr = bmpdata.getBGR()
    for hei in range(bmpdata.getheight()):
        for wid in range(bmpdata.getwidth()):
            calc = int(0.298912*arr[wid][hei][2] + 0.586611*arr[wid][hei][1] + 0.114478*arr[wid][hei][0])
            arr[wid][hei] = [calc, calc, calc]
    bmpdata.setBGR(arr)
    print("Greyscaled (NTSC Coef. method) the file")

def invertColors(bmpdata):
    arr = bmpdata.getBGR()
    for hei in range(bmpdata.getheight()):
        for wid in range(bmpdata.getwidth()):
            arr[wid][hei] = [abs(255 - arr[wid][hei][0]),
                             abs(255 - arr[wid][hei][1]),
                             abs(255 - arr[wid][hei][2])]
    bmpdata.setBGR(arr)
    print("Inverted the color")

def blurImage(bmpdata):
    arr = bmpdata.getBGR()
    arr_mod = getEmptyArray(bmpdata.getwidth(), bmpdata.getheight())
    for hei in range(bmpdata.getheight()):
        for wid in range(bmpdata.getwidth()):
            sum_b = arr[wid][hei][0]
            sum_g = arr[wid][hei][1]
            sum_r = arr[wid][hei][2]
            count = 1   # 割る数
            # 周囲ピクセルが範囲外の場合に除外
            if wid - 1 >= 0:
                sum_b += arr[wid-1][hei][0]
                sum_g += arr[wid-1][hei][1]
                sum_r += arr[wid-1][hei][2]
                count += 1
            if wid + 1 < bmpdata.getwidth():
                sum_b += arr[wid+1][hei][0]
                sum_g += arr[wid+1][hei][1]
                sum_r += arr[wid+1][hei][2]
                count += 1
            if hei - 1 >= 0:
                sum_b += arr[wid][hei-1][0]
                sum_g += arr[wid][hei-1][1]
                sum_r += arr[wid][hei-1][2]
                count += 1
            if hei + 1 < bmpdata.getheight():
                sum_b += arr[wid][hei+1][0]
                sum_g += arr[wid][hei+1][1]
                sum_r += arr[wid][hei+1][2]
                count += 1

            arr_mod[wid][hei] = [sum_b // count, sum_g // count, sum_r // count]

    bmpdata.setBGR(arr_mod)
    print("Blured the image")


def getEmptyArray(width, height):
    return [[0 for i in range(height)] for j in range(width)]


if __name__ == '__main__':
    main()
    print("FINISHED!\n")
