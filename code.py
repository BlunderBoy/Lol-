import pytesseract
from PIL import ImageGrab
import os
import time
import win32api
import win32con
import numpy as np
import ast
import keyboard

# Globals
# ------------------
#x_pad = 582
#y_pad = 366
# 330 140 1660 1020


class Database:
    def __init__(self):
        self.dict = dict()

    def readDict(self, file):
        fisier = open(file, "r")
        content = fisier.read()
        self.dict = ast.literal_eval(content)
        fisier.close()

    def saveDict(self, file):
        fisier = open(file, "w")
        print(self.dict, file=fisier)

def toGrayscale(image):
    return image.convert("L")


def toNpArray(image):
    return np.asarray(image)

def mousePos(cord):
    win32api.SetCursorPos(x_pad + cord[0], y_pad + cord[1])

def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x,y)

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    print("Click.")  # completely optional. But nice for debugging purposes.


def screenGrab():
    box = (320, 130, 1650, 950)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\screenshots\\snap__' + str(int(time.time())) +
            '.png', 'PNG')
    return im


def main():
    #get_cords()
    while True:
        if keyboard.is_pressed("f2"):
            pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            im = screenGrab()
            im = im.resize((2660, 1640))
            im.save(os.getcwd() + '\\screenshots\\resized__' + str(int(time.time())) +
                    '.png', 'PNG')
            txt = pytesseract.image_to_string(im)
            print(txt)
            
    #print(pytesseract.image_to_string(
    #    r'C:\Users\Liviu.LIVIU-PC.000\Desktop\bot\snap__1603558076.png'))


if __name__ == '__main__':
    main()

# play again: 91 -5
