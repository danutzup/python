# glcd12864.py
import os
import time
import RPi.GPIO as GPIO
import math

class GLCD12864:

    char3x5 = [                                     # KEY   | ASCII(dec)
        [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],    # SPACE     32
        [[1,1,1,0,1]],                              # !         33
        [[1,1,0,0,0], [0,0,0,0,0], [1,1,0,0,0]],    # "         34
        [[1,1,1,1,1], [0,1,0,1,0], [1,1,1,1,1]],    # #         35
        [[0,1,0,1,0], [1,1,1,1,1], [1,0,1,0,0]],    # $         36
        [[1,0,0,1,0], [0,0,1,0,0], [0,1,0,0,1]],    # %         37
        [[1,1,1,1,0], [1,1,1,0,1], [0,0,1,1,1]],    # &         38
        [[1,1,0,0,0]],                              # '         39
        [[0,1,1,1,0], [1,0,0,0,1]],                 # (         40
        [[1,0,0,0,1], [0,1,1,1,0]],                 # )         41
        [[1,0,1,0,0], [0,1,0,0,0], [1,0,1,0,0]],    # *         42
        [[0,0,1,0,0], [0,1,1,1,0], [0,0,1,0,0]],    # +         43
        [[0,0,0,0,1], [0,0,0,1,0]],                 # ,         44
        [[0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0]],    # -         45
        [[0,0,0,0,1]],                              # .         46
        [[0,0,0,1,1], [0,0,1,0,0], [1,1,0,0,0]],    # /         47
        [[1,1,1,1,1], [1,0,0,0,1], [1,1,1,1,1]],    # 0         48
        [[1,0,0,0,1], [1,1,1,1,1], [0,0,0,0,1]],    # 1         49
        [[1,0,1,1,1], [1,0,1,0,1], [1,1,1,0,1]],    # 2         50
        [[1,0,1,0,1], [1,0,1,0,1], [1,1,1,1,1]],    # 3         51
        [[1,1,1,0,0], [0,0,1,0,0], [1,1,1,1,1]],    # 4         52
        [[1,1,1,0,1], [1,0,1,0,1], [1,0,1,1,1]],    # 5         53
        [[1,1,1,1,1], [1,0,1,0,1], [1,0,1,1,1]],    # 6         54
        [[1,0,0,0,0], [1,0,0,1,1], [1,1,1,0,0]],    # 7         55
        [[1,1,1,1,1], [1,0,1,0,1], [1,1,1,1,1]],    # 8         56
        [[1,1,1,0,1], [1,0,1,0,1], [1,1,1,1,1]],    # 9         57
        [[0,1,0,1,0]],                              # :         58
        [[0,0,0,0,1], [0,1,0,1,0]],                 # ;         59
        [[0,0,1,0,0], [0,1,0,1,0], [1,0,0,0,1]],    # <         60
        [[0,1,0,1,0], [0,1,0,1,0], [0,1,0,1,0]],    # =         61
        [[1,0,0,0,1], [0,1,0,1,0], [1,1,1,1,1]],    # >         62
        [[1,0,0,0,0], [1,0,1,0,1], [1,1,0,0,0]],    # ?         63
        [[0,1,1,1,0], [1,0,1,0,1], [0,1,1,0,1]],    # @         64
        [[1,1,1,1,1], [1,0,1,0,0], [1,1,1,1,1]],    # A         65
        [[1,1,1,1,1], [1,0,1,0,1], [0,1,0,1,0]],    # B         66
        [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1]],    # C         67
        [[1,1,1,1,1], [1,0,0,0,1], [0,1,1,1,0]],    # D         68
        [[1,1,1,1,1], [1,0,1,0,1], [1,0,1,0,1]],    # E         69
        [[1,1,1,1,1], [1,0,1,0,0], [1,0,1,0,0]],    # F         70
        [[0,1,1,1,0], [1,0,1,0,1], [1,0,1,1,1]],    # G         71
        [[1,1,1,1,1], [0,0,1,0,0], [1,1,1,1,1]],    # H         72
        [[1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1]],    # I         73
        [[0,0,0,1,0], [0,0,0,0,1], [1,1,1,1,0]],    # J         74
        [[1,1,1,1,1], [0,0,1,0,0], [1,1,0,1,1]],    # K         75
        [[1,1,1,1,1], [0,0,0,0,1], [0,0,0,0,1]],    # L         76
        [[1,1,1,1,1], [0,1,1,0,0], [1,1,1,1,1]],    # M         77
        [[1,1,1,1,1], [0,1,1,1,0], [1,1,1,1,1]],    # N         78
        [[0,1,1,1,0], [1,0,0,0,1], [0,1,1,1,0]],    # O         79
        [[1,1,1,1,1], [1,0,1,0,0], [0,1,0,0,0]],    # P         80
        [[0,1,1,1,0], [1,0,0,1,1], [0,1,1,1,1]],    # Q         81
        [[1,1,1,1,1], [1,0,1,0,0], [0,1,0,1,1]],    # R         82
        [[0,1,0,0,1], [1,0,1,0,1], [1,0,0,1,0]],    # S         83
        [[1,0,0,0,0], [1,1,1,1,1], [1,0,0,0,0]],    # T         84
        [[1,1,1,1,1], [0,0,0,0,1], [1,1,1,1,1]],    # U         85
        [[1,1,1,1,0], [0,0,0,0,1], [1,1,1,1,0]],    # V         86
        [[1,1,1,1,1], [0,0,1,1,0], [1,1,1,1,1]],    # W         87
        [[1,1,0,1,1], [0,0,1,0,0], [1,1,0,1,1]],    # X         88
        [[1,1,0,0,0], [0,0,1,1,1], [1,1,0,0,0]],    # Y         89
        [[1,0,0,1,1], [1,0,1,0,1], [1,1,0,0,1]],    # Z         90
        [[1,1,1,1,1], [1,0,0,0,1]],                 # [         91
        [[1,1,0,0,0], [0,0,1,0,0], [0,0,0,1,1]],    # \         92
        [[1,0,0,0,1], [1,1,1,1,1]],                 # ]         93
        [[0,1,0,0,0], [1,0,0,0,0], [0,1,0,0,0]],    # ^         94
        [[0,0,0,0,1], [0,0,0,0,1], [0,0,0,0,1]],    # _         95
        [[1,1,0,0,0]],                              # '         96
        [[0,1,0,1,1], [0,1,1,0,1], [0,0,1,1,1]],    # a         97
        [[1,1,1,1,1], [0,1,0,0,1], [0,0,1,1,0]],    # b         98
        [[0,0,1,1,0], [0,1,0,0,1], [0,1,0,0,1]],    # c         99
        [[0,0,1,1,0], [0,1,0,0,1], [1,1,1,1,1]],    # d         100
        [[0,0,1,1,0], [0,1,0,1,1], [0,1,1,0,1]],    # e         101
        [[0,0,1,0,0], [0,1,1,1,1], [1,0,1,0,0]],    # f         102
        [[0,1,1,0,0], [1,0,1,0,1], [1,1,1,1,0]],    # g         103
        [[1,1,1,1,1], [0,1,0,0,0], [0,0,1,1,1]],    # h         104
        [[1,0,1,1,1]],                              # i         105
        [[0,0,0,1,0], [0,0,0,0,1], [1,0,1,1,1]],    # j         106
        [[1,1,1,1,1], [0,0,1,1,0], [0,1,0,0,1]],    # k         107
        [[1,0,0,0,1], [1,1,1,1,1], [0,0,0,0,1]],    # l         108
        [[0,1,1,1,1], [0,1,1,1,0], [0,1,1,1,1]],    # m         109
        [[0,1,1,1,1], [0,1,0,0,0], [0,1,1,1,1]],    # n         110
        [[0,0,1,1,0], [0,1,0,0,1], [0,0,1,1,0]],    # o         111
        [[0,1,1,1,1], [0,1,0,1,0], [0,0,1,0,0]],    # p         112
        [[0,0,1,0,0], [0,1,0,1,0], [0,1,1,1,1]],    # q         113
        [[0,0,1,1,1], [0,1,0,0,0], [0,1,1,0,0]],    # r         114
        [[0,0,1,0,1], [0,1,1,1,1], [0,1,0,1,0]],    # s         115
        [[0,1,0,0,0], [1,1,1,1,1], [0,1,0,0,1]],    # t         116
        [[0,1,1,1,1], [0,0,0,0,1], [0,1,1,1,1]],    # u         117
        [[0,1,1,1,0], [0,0,0,0,1], [0,1,1,1,0]],    # v         118
        [[0,1,1,1,1], [0,0,1,1,1], [0,1,1,1,1]],    # w         119
        [[0,1,0,0,1], [0,0,1,1,0], [0,1,0,0,1]],    # x         120
        [[0,1,1,0,1], [0,0,0,1,1], [0,1,1,1,0]],    # y         121
        [[0,1,0,1,1], [0,1,1,1,1], [0,1,1,0,1]],    # z         122
        [[0,0,1,0,0], [1,1,0,1,1], [1,0,0,0,1]],    # {         123
        [[1,1,1,1,1]],                              # |         124
        [[1,0,0,0,1], [1,1,0,1,1], [0,0,1,0,0]],    # ]         125
        [[0,0,1,0,0], [0,1,1,0,0], [0,1,0,0,0]],    # ~         126
        [[1,0,1,0,1], [0,1,0,1,0], [1,0,1,0,1]]]    # ERROR     "127" = If the ascii is out of range,
                                                    # will print this custom char instead.

    cz2 = {
        345: 128, 237: 129, 353: 130, 382: 131, 357: 132, 269: 133, 253: 134,
        367: 135, 328: 136, 250: 137, 283: 138, 271: 139, 225: 140, 233: 141,
        243: 142, 344: 143, 205: 144, 352: 145, 381: 146, 356: 147, 268: 148,
        221: 149, 366: 150, 327: 151, 218: 152, 282: 153, 270: 154, 193: 155,
        201: 156, 211: 157, 228: 228, 235: 235, 239: 239, 246: 246, 252: 252,
        196: 196, 214: 214, 220: 220, 176: 176, 177: 177, 171: 171, 166: 166,
        223: 223
    }

    sData_Pin = 7
    sClk_Pin = 8
    reset_Pin = 25

    def __init__(self):
        self.mapa = {}
        self.txtmapa = {}
        self.font2 = {}
        self.iconData = {}

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sData_Pin, GPIO.OUT)
        GPIO.setup(self.sClk_Pin, GPIO.OUT)
        GPIO.setup(self.reset_Pin, GPIO.OUT)
        GPIO.output(self.sData_Pin, False)
        GPIO.output(self.sClk_Pin, False)
        GPIO.output(self.reset_Pin, False)
        time.sleep(0.1)
        GPIO.output(self.reset_Pin, True)
        self.loadTextFont("font2.txt")

    def quickSleep(self):
        time.sleep(0)

    def strobe(self):
        GPIO.output(self.sClk_Pin, True)
        self.quickSleep()
        GPIO.output(self.sClk_Pin, False)

    def strobe4(self):
        for _ in range(4):
            self.strobe()

    def strobe5(self):
        for _ in range(5):
            self.strobe()

    def setDataPin(self, bit):
        GPIO.output(self.sData_Pin, bit)

    def send2Bytes(self, rs, byte1, byte2):
        self.setDataPin(1)
        self.strobe5()
        self.setDataPin(0)
        self.strobe()
        self.setDataPin(rs)
        self.strobe()
        self.setDataPin(0)
        self.strobe()
        for i in range(7, 3, -1):
            self.setDataPin(byte1 & (1 << i))
            self.strobe()
        self.setDataPin(0)
        self.strobe4()
        for i in range(3, -1, -1):
            self.setDataPin(byte1 & (1 << i))
            self.strobe()
        self.setDataPin(0)
        self.strobe4()
        for i in range(7, 3, -1):
            self.setDataPin(byte2 & (1 << i))
            self.strobe()
        self.setDataPin(0)
        self.strobe4()
        for i in range(3, -1, -1):
            self.setDataPin(byte2 & (1 << i))
            self.strobe()
        self.setDataPin(0)
        self.strobe4()

    def sendByte(self, rs, byte):
        self.setDataPin(1)
        self.strobe5()
        self.setDataPin(0)
        self.strobe()
        self.setDataPin(rs)
        self.strobe()
        self.setDataPin(0)
        self.strobe()
        for i in range(7, 3, -1):
            self.setDataPin(byte & (1 << i))
            self.strobe()
        self.setDataPin(0)
        self.strobe4()
        for i in range(3, -1, -1):
            self.setDataPin(byte & (1 << i))
            self.strobe()
        self.setDataPin(0)
        self.strobe4()

    def plot(self, posX, posY, style=1):
        if posX > 127: posX = 127
        elif posX < 0: posX = 0
        if posY > 63: posY = 63
        elif posY < 0: posY = 0
        horiz = posX // 16
        if posY >= 32:
            posY -= 32
            horiz += 8
        minibit = posX & 15
        self.send2Bytes(0, 0b10000000 + posY, 0b10000000 + horiz)
        originalLeftByte = self.mapa.get((horiz, posY, 0), 0)
        originalRightByte = self.mapa.get((horiz, posY, 1), 0)
        if minibit < 8:
            if style == 1:
                leftByte = (0b10000000 >> minibit) | originalLeftByte
            elif style == 0:
                leftByte = ~(0b10000000 >> minibit) & originalLeftByte
            else:
                leftByte = (0b10000000 >> minibit) ^ originalLeftByte
            self.mapa[horiz, posY, 0] = leftByte
            rightByte = originalRightByte
        else:
            if style == 1:
                rightByte = (0b10000000 >> (minibit-8)) | originalRightByte
            elif style == 0:
                rightByte = ~(0b10000000 >> (minibit-8)) & originalRightByte
            else:
                rightByte = (0b10000000 >> (minibit-8)) ^ originalRightByte
            self.mapa[horiz, posY, 1] = rightByte
            leftByte = originalLeftByte
        self.send2Bytes(1, leftByte, rightByte)

    def loadTextFont(self, fileName):
        script_path = os.path.abspath(__file__)
        script_dir = os.path.split(script_path)[0]
        fullPathFileName = os.path.join(script_dir, fileName)
        fontfile = open(fullPathFileName, "r")
        adresafontu = 0
        for row in fontfile:
            rozlozeno = row.split(",")
            for byte in range(8):
                self.font2[adresafontu] = int(rozlozeno[byte][-4:], 0)
                adresafontu = adresafontu + 1
        fontfile.close()

    def clearDisplay(self, pattern=0):
        self.clearGraphic(pattern)
        self.clearText()

    def clearGraphic(self, pattern=0):
        self.initGraphicMode()
        self.sendByte(0, 0b00110110)
        self.sendByte(0, 0b00110100)
        self.sendByte(0, 0b00001000)
        for vertical in range(32):
            self.send2Bytes(0, 0b10000000 + vertical, 0b10000000)
            for horizontal in range(16):
                self.send2Bytes(1, pattern, pattern)
                self.mapa[horizontal, vertical, 0] = pattern
                self.mapa[horizontal, vertical, 1] = pattern
        self.sendByte(0, 0b00110110)

    def clearText(self):
        self.sendByte(0, 0b00110000)
        self.sendByte(0, 0b00110000)
        self.sendByte(0, 0b00001100)
        self.sendByte(0, 0b00000001)
        self.txtmapa[0] = "                "
        self.txtmapa[1] = "                "
        self.txtmapa[2] = "                "
        self.txtmapa[3] = "                "

    def initGraphicMode(self):
        self.sendByte(0, 0b00110010)
        self.sendByte(0, 0b00110110)
        self.sendByte(0, 0b00110110)
        self.sendByte(0, 0b00000010)

    def initTextMode(self):
        self.sendByte(0, 0b00110000)
        self.sendByte(0, 0b00110100)
        self.sendByte(0, 0b00110110)
        self.sendByte(0, 0b00000010)
        self.sendByte(0, 0b00110000)
        self.sendByte(0, 0b00001100)
        self.sendByte(0, 0b10000000)

    def printStringTextMode(self, string, column, row):
        if len(string) + column > 16:
            string = string[0:16 - column]
        self.setTextCursorPos(column, row)
        for idx, char in enumerate(string):
            self.sendByte(1, ord(char))
            pomtext = self.txtmapa[row][:column + idx] + char + self.txtmapa[row][column + idx + 1:]
            self.txtmapa[row] = pomtext

    def setTextCursorPos(self, column, row):
        shift = column
        if row == 1: shift = column + 32
        if row == 2: shift = column + 16
        if row == 3: shift = column + 48
        self.sendByte(0, 0b10000000 + int(shift / 2))
        if column / 2.0 != column / 2:
            orignal_predcharacter = self.txtmapa[row][column - 1:column]
            self.sendByte(1, ord(orignal_predcharacter))

    def cleanup(self):
        GPIO.cleanup()
