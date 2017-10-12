# coding: UTF-8
# Tested on Python 3.6.3 (32bit)
# This program converts ./gazou1.bmp to ./gazou2.bmp

import sys
import struct
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

class BmpFile:
    def __init__(self):
        self.idchara = bytes()
        self.filesize = bytes()
        self.res_a = bytes()
        self.res_b = bytes()
        self.headersize = bytes()
        self.infosize = bytes()
        self.width = bytes()
        self.height = bytes()
        self.pixnum = bytes()
        self.colordepth = bytes()
        self.compmethod = bytes()
        self.compsize = bytes()
        self.horizonalres = bytes()
        self.verticalres = bytes()
        self.colornum = bytes()
        self.impcolornum = bytes()
        self.color_r = []
        self.color_g = []
        self.color_b = []

    def read(self, bmpfile):
        self.idchara = bmpfile.read(2)
        self.filesize = bmpfile.read(4)
        self.res_a = bmpfile.read(2)
        self.res_b = bmpfile.read(2)
        self.headersize = bmpfile.read(4)
        self.infosize = bmpfile.read(4)
        self.width = bmpfile.read(4)
        self.height = bmpfile.read(4)
        self.pixnum = bmpfile.read(2)
        self.colordepth = bmpfile.read(2)
        self.compmethod = bmpfile.read(4)
        self.compsize = bmpfile.read(4)
        self.horizonalres = bmpfile.read(4)
        self.verticalres = bmpfile.read(4)
        self.colornum = bmpfile.read(4)
        self.impcolornum = bmpfile.read(4)
        
        tmp = 0
        while 1 :
            readtmp = bmpfile.read(1)
            if readtmp == b'':
                break

            if tmp == 0:
                self.color_b.append(readtmp)
                tmp += 1
            elif tmp == 1:
                self.color_g.append(readtmp)
                tmp += 1
            elif tmp == 2:
                self.color_r.append(readtmp)
                tmp = 0

    def write(self, filepath):
        try:
            bmpdata = open(filepath, 'wb')
            bmpdata.write(self.idchara)
            bmpdata.write(self.filesize)
            bmpdata.write(self.res_a)
            bmpdata.write(self.res_b)
            bmpdata.write(self.headersize)
            bmpdata.write(self.infosize)
            bmpdata.write(self.width)
            bmpdata.write(self.height)
            bmpdata.write(self.pixnum)
            bmpdata.write(self.colordepth)
            bmpdata.write(self.compmethod)
            bmpdata.write(self.compsize)
            bmpdata.write(self.horizonalres)
            bmpdata.write(self.verticalres)
            bmpdata.write(self.colornum)
            bmpdata.write(self.impcolornum)

            for i in range(len(self.color_b)):
                bmpdata.write(self.color_b[i])
                bmpdata.write(self.color_g[i])
                bmpdata.write(self.color_r[i])

            bmpdata.close()
        except():
            print("OPEN ERROR")

def main():
    print("Convert ./gazou1.bmp to ./gazou2.bmp")
    print("1 - Greyscale (Middle value)")
    print("2 - Greyscale (NTSC Coef. method)")
    keyinput = input("Please type the number: ")
    
    bmpdata = readBMP(r".\gazou1.bmp")
    if int(keyinput) == 1:
        convertToGreyscale1(bmpdata)
    elif int(keyinput) == 2:
        convertToGreyscale2(bmpdata)
        
    writeBMP(r".\gazou2.bmp", bmpdata)
    

def readBMP(filepath):
    bmpdata = BmpFile()
    bmpdata.read(open(filepath, 'rb'))
    print("Read the file")

    return bmpdata


def writeBMP(filepath, bmpdata):
    bmpdata.write(filepath)
    print("Wrote the file")
    return


def convertToGreyscale1(bmpdata):
    # middle value
    for i in range(len(bmpdata.color_b)):
        bmax = max(bmpdata.color_b[i], bmpdata.color_g[i], bmpdata.color_r[i])
        bmin = min(bmpdata.color_b[i], bmpdata.color_g[i], bmpdata.color_r[i])
        grayint = (int.from_bytes(bmax, 'little') + int.from_bytes(bmin, 'little') ) // 2
        bmpdata.color_b[i] = bmpdata.color_g[i] = bmpdata.color_r[i] = grayint.to_bytes(1, 'little')
    print("Greyscaled (Middle value) the file")

def convertToGreyscale2(bmpdata):
    # NTSC Coef. method
    for i in range(len(bmpdata.color_b)):
        blueint = int.from_bytes(bmpdata.color_b[i], 'little')
        greenint = int.from_bytes(bmpdata.color_g[i], 'little')
        redint = int.from_bytes(bmpdata.color_r[i], 'little')
        grayfloat = 0.298912 * redint + 0.586611 * greenint + 0.114478 * blueint
        bmpdata.color_b[i] = bmpdata.color_g[i] = bmpdata.color_r[i] = int(grayfloat).to_bytes(1, 'little')
    print("Greyscaled (NTSC Coef. method) the file")
    
if __name__ == '__main__':
    main()
    print("FINISHED")
