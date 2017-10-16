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

        setcolor = 0
        p_wid = 0
        wid = self.getwidth()
        padding = self.getpaddingbytesize()
        
        while 1:
            if p_wid < wid:
                readtmp = bmpfile.read(1)
                # ファイル終了時break
                if readtmp == b'':
                    break
                readtmpint = int.from_bytes(readtmp, 'little')
                if setcolor == 0:
                    self.__color_b.append(readtmpint)
                    setcolor += 1
                elif setcolor == 1:
                    self.__color_g.append(readtmpint)
                    setcolor += 1
                elif setcolor == 2:
                    self.__color_r.append(readtmpint)
                    setcolor = 0
                    p_wid += 1
            else:
                if padding != 0:
                    readtmp = bmpfile.read(padding)
                p_wid = 0

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

            wid = self.getwidth()
            for i in range(len(self.__color_b)):
                bmpdata.write(self.__color_b[i].to_bytes(1, 'little'))
                bmpdata.write(self.__color_g[i].to_bytes(1, 'little'))
                bmpdata.write(self.__color_r[i].to_bytes(1, 'little'))
                if i % wid == wid - 1 and self.getpaddingbytesize() != 0:
                    for _ in range(4 - self.getpaddingbytesize()):
                        bmpdata.write(b'\x00')
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
        self.__color_b.clear()
        self.__color_g.clear()
        self.__color_r.clear()
        for hei in range(self.getheight()):
            for wid in range(self.getwidth()):
                self.__color_b.append(arr[wid][hei][0])
                self.__color_g.append(arr[wid][hei][1])
                self.__color_r.append(arr[wid][hei][2])

    def setWH(self, newwid, newhei):
        self.__width = newwid.to_bytes(4, 'little')
        self.__height = newhei.to_bytes(4, 'little')

    def getpaddingbytesize(self):
        """ returns necessary padding bytes """
        return (self.getwidth() * 3) % 4


def main():
    print("\nConvert {} to {}".format(READPATH, WRITEPATH))
    print("1 - Greyscale (Middle value)")
    print("2 - Greyscale (NTSC Coef. method)")
    print("3 - Color Inversion")
    print("4 - Blur")
    print("5 - Scaling")
    print("6 - Binarize")
    keyinput = input("\nPlease type the number: ")
    
    bmpdata = BmpFile()

    # readBMP
    rfile = open(READPATH, 'rb')
    bmpdata.read(rfile)
    rfile.close()
    print("Read the file")

    # Image Processing
    if int(keyinput) == 1:
        convertToGreyscale1(bmpdata)
        print("Greyscaled (Middle value) the file")
    elif int(keyinput) == 2:
        convertToGreyscale2(bmpdata)
        print("Greyscaled (NTSC Coef. method) the file")
    elif int(keyinput) == 3:
        invertColors(bmpdata)
        print("Inverted the color")
    elif int(keyinput) == 4:
        blurImage(bmpdata)
        print("Blured the image")
    elif int(keyinput) == 5:
        scaleImage(bmpdata)
        print("Scaled the image")
    elif int(keyinput) == 6:
        binaryImage(bmpdata)
        print("Binarized the image")

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

def convertToGreyscale2(bmpdata):
    """ NTSC Coef. method """
    arr = bmpdata.getBGR()
    for hei in range(bmpdata.getheight()):
        for wid in range(bmpdata.getwidth()):
            calc = int(0.298912*arr[wid][hei][2] + 0.586611*arr[wid][hei][1] + 0.114478*arr[wid][hei][0])
            arr[wid][hei] = [calc, calc, calc]
    bmpdata.setBGR(arr)

def invertColors(bmpdata):
    arr = bmpdata.getBGR()
    for hei in range(bmpdata.getheight()):
        for wid in range(bmpdata.getwidth()):
            arr[wid][hei] = [abs(255 - arr[wid][hei][0]),
                             abs(255 - arr[wid][hei][1]),
                             abs(255 - arr[wid][hei][2])]
    bmpdata.setBGR(arr)

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

def scaleImage(bmpdata):
    scale = float(input("Input scaling rate: "))
    arr = bmpdata.getBGR()
    scaled_width = round(bmpdata.getwidth() * scale)
    scaled_height = round(bmpdata.getheight() * scale)
    arr_mod = getEmptyArray(scaled_width, scaled_height)

    for hei in range(scaled_height):
        for wid in range(scaled_width):
            x = round(wid / scale)
            y = round(hei / scale)
            if x < bmpdata.getwidth() and y < bmpdata.getheight():
                arr_mod[wid][hei] = arr[x][y]
            else:
                arr_mod[wid][hei] = [0, 0, 0]

    bmpdata.setWH(scaled_width, scaled_height)
    bmpdata.setBGR(arr_mod)


def binaryImage(bmpdata):
    threshold = int(input("Input threshold (0 - 255): "))
    if threshold < 0 or threshold > 255:
        threshold = 127
    convertToGreyscale2(bmpdata)
    arr = bmpdata.getBGR()
    for hei in range(bmpdata.getheight()):
        for wid in range(bmpdata.getwidth()):
            if arr[wid][hei][0] > threshold:
                arr[wid][hei] = [255, 255, 255]
            else:
                arr[wid][hei] = [0, 0, 0]
    bmpdata.setBGR(arr)


def getEmptyArray(width, height):
    return [[0 for i in range(height)] for j in range(width)]


if __name__ == '__main__':
    main()
    print("FINISHED!\n")
