# coding: UTF-8
# Tested on Python 3.6.3 (32bit)
# This program converts ./gazou1.bmp to ./gazou2.bmp

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
        self.w = int()
        self.h = int()

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
        
        self.w = int.from_bytes(self.width, 'little')
        self.h = int.from_bytes(self.height, 'little')
        
        tmp = 0
        while 1 :
            readtmp = bmpfile.read(1)
            if readtmp == b'':
                break
            readtmpint = int.from_bytes(readtmp, 'little')
            if tmp == 0:
                self.color_b.append(readtmpint)
                tmp += 1
            elif tmp == 1:
                self.color_g.append(readtmpint)
                tmp += 1
            elif tmp == 2:
                self.color_r.append(readtmpint)
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
                bmpdata.write(self.color_b[i].to_bytes(1, 'little'))
                bmpdata.write(self.color_g[i].to_bytes(1, 'little'))
                bmpdata.write(self.color_r[i].to_bytes(1, 'little'))

            bmpdata.close()
        except():
            print("OPEN ERROR")
            exit()
    
    def getArray(self):
        arr_b = [[0 for i in range(self.h)] for j in range(self.w)]
        arr_g = [[0 for i in range(self.h)] for j in range(self.w)]
        arr_r = [[0 for i in range(self.h)] for j in range(self.w)]
        for i in range(len(self.color_b)):
            arr_b[i%self.w][i//self.w] = self.color_b[i]
        for i in range(len(self.color_g)):
            arr_g[i%self.w][i//self.w] = self.color_g[i]
        for i in range(len(self.color_r)):
            arr_r[i%self.w][i//self.w] = self.color_r[i]
        return [arr_b, arr_g, arr_r]

    def setArray(self, arr_b, arr_g, arr_r):
        i = 0
        for he in range(self.h):
            for wi in range(self.w):
                self.color_b[i] = arr_b[wi][he]
                self.color_g[i] = arr_g[wi][he]
                self.color_r[i] = arr_r[wi][he]
                i += 1

    def getEmptyArray(self):
        return [[0 for i in range(self.h)] for j in range(self.w)]


def main():
    print("Convert ./gazou1.bmp to ./gazou2.bmp")
    print("1 - Greyscale (Middle value)")
    print("2 - Greyscale (NTSC Coef. method)")
    print("3 - Color Inversion")
    print("4 - Blur")
    keyinput = input("Please type the number: ")
    
    bmpdata = readBMP(r"./gazou1.bmp")
    if int(keyinput) == 1:
        convertToGreyscale1(bmpdata)
    elif int(keyinput) == 2:
        convertToGreyscale2(bmpdata)
    elif int(keyinput) == 3:
        invertColors(bmpdata)
    elif int(keyinput) == 4:
        blurImage(bmpdata)
    writeBMP(r"./gazou2.bmp", bmpdata)
    

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
        bmpdata.color_b[i] = bmpdata.color_g[i] = bmpdata.color_r[i] = ( bmax + bmin ) // 2
    print("Greyscaled (Middle value) the file")


def convertToGreyscale2(bmpdata):
    # NTSC Coef. method
    for i in range(len(bmpdata.color_b)):
        bmpdata.color_b[i] = bmpdata.color_g[i] = bmpdata.color_r[i] = \
            int(0.298912 * bmpdata.color_r[i] + 0.586611 * bmpdata.color_g[i] + 0.114478 * bmpdata.color_b[i])
    print("Greyscaled (NTSC Coef. method) the file")


def invertColors(bmpdata):
    for i in range(len(bmpdata.color_b)):
        # 念のため絶対値
        bmpdata.color_b[i] = abs(255 - bmpdata.color_b[i])
        bmpdata.color_g[i] = abs(255 - bmpdata.color_g[i])
        bmpdata.color_r[i] = abs(255 - bmpdata.color_r[i])
    print("Inverted the color")


def blurImage(bmpdata):
    #ぼかし
    arr_b, arr_g, arr_r = bmpdata.getArray()
    arr_b_mod = bmpdata.getEmptyArray()
    arr_g_mod = bmpdata.getEmptyArray()
    arr_r_mod = bmpdata.getEmptyArray()
    width = bmpdata.w
    height = bmpdata.h
    for h in range(height):
        for w in range(width):
            sum_b = arr_b[w][h]
            sum_g = arr_g[w][h]
            sum_r = arr_r[w][h]
            count = 1
            # 周囲ピクセル範囲外の場合
            if w - 1 >= 0:
                sum_b += arr_b[w-1][h]
                sum_g += arr_g[w-1][h]
                sum_r += arr_r[w-1][h]
                count += 1
            if w + 1 < width:
                sum_b += arr_b[w+1][h]
                sum_g += arr_g[w+1][h]
                sum_r += arr_r[w+1][h]
                count += 1
            if h - 1 >= 0:
                sum_b += arr_b[w][h-1]
                sum_g += arr_g[w][h-1]
                sum_r += arr_r[w][h-1]
                count += 1
            if h + 1 < height:
                sum_b += arr_b[w][h+1]
                sum_g += arr_g[w][h+1]
                sum_r += arr_r[w][h+1]
                count += 1
                
            arr_b_mod[w][h] = (sum_b // count)
            arr_g_mod[w][h] = (sum_g // count)
            arr_r_mod[w][h] = (sum_r // count)
            
    bmpdata.setArray(arr_b_mod, arr_g_mod, arr_r_mod)
    print("Blured the image")


if __name__ == '__main__':
    main()
    print("FINISHED")
