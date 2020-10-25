from numpy.lib.function_base import append, vectorize
import pytesseract
from PIL import ImageGrab, Image
import os
import time
import win32api
import win32con
import numpy as np
import ast
import keyboard
from fuzzy_types.fuzzy import FuzzyDict
import pprint

# Globals
# ------------------
#x_pad = 582
#y_pad = 366
# 330 140 1660 1020

class Database:
    def __init__(self):
        self.dict = FuzzyDict({})

    def readDict(self, file):
        fisier = open(file, "r")
        content = fisier.read()
        self.dict = ast.literal_eval(content)
        fisier.close()

    def saveDict(self, file):
        fisier = open(file, "w")
        pp = pprint.PrettyPrinter(indent=4, stream=fisier)
        pp.pprint(self.dict)

    def addEntry(self, question, correctAnswer, wrongAnswer1, wrongAnswer2):
        self.dict[question] = (correctAnswer, wrongAnswer1, wrongAnswer2)

    def lookup(self, question):
        return self.dict[question]

def toGrayscale(image):
    return image.convert("L")

def toNpArray(image):
    return np.asarray(image)

def mousePos(cord):
    win32api.SetCursorPos(cord[0], cord[1])

def get_cords():
    x, y = win32api.GetCursorPos()
    print(x,y)

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    print("Click.")  # completely optional. But nice for debugging purposes.


def screenGrab():
    box = (320, 130, 1650, 950)
    im = ImageGrab.grab(box)
    return im

def getList(txt):
    lista = list(filter(lambda a: a != "" and a != "\x0c", txt.split('\n')))
    if len(lista) > 4:
        listuta = []
        listuta.append(lista[0] + " " + lista[1])
        listuta = listuta + lista[2::]
        return listuta
    return lista

def saveImage(image):
    image.save(os.getcwd() + '\\screenshots\\original__' + str(int(time.time())) +
                    '.png', 'PNG')

def saveImageRes(image):
    image.save(os.getcwd() + '\\screenshots\\resized__' + str(int(time.time())) +
                    '.png', 'PNG')


def binarize(image_to_transform, threshold):
    for x in range(image_to_transform.width):
        for y in range(image_to_transform.height):
            # for the given pixel at w,h, lets check its value against the threshold
            if image_to_transform.getpixel((x,y)) < threshold: #note that the first parameter is actually a tuple object
                # lets set this to zero
                image_to_transform.putpixel((x,y), 0)
            else:
                # otherwise lets set this to 255
                image_to_transform.putpixel((x,y), 255)
    #now we just return the new image
    return image_to_transform

def removeNoise(image):
    image = toGrayscale(image)
    finalImage = image.resize((2660, 1640))
    finalImage = binarize(image, 58)
    return finalImage

def main():
    #get_cords()
    database = Database()
    try:
        database.readDict("dictionar.txt")
    except:
        pass

    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    while True:
        if keyboard.is_pressed("f2"):
            #save original image
            im = screenGrab()
            saveImage(im)
            
            #save noise removed image
            new = removeNoise(im)
            saveImageRes(new)

            print(pytesseract.image_to_string(new))

        if keyboard.is_pressed("f7"):
            im = removeNoise(screenGrab())
            list = getList(pytesseract.image_to_string(im))
            saveImageRes(im)

            if len(list) < 4:
                print(list)
                print("Ceva nu a mers bine la text recognition")
                continue

            print(list)
            question = list[0]
            answers = list[1::] 

            corect = int(input("Care e corect?")) - 1
            set = [0,1,2]
            set.remove(corect)
            database.addEntry(question, answers[corect], answers[set[0]], answers[set[1]])

        if keyboard.is_pressed("f6"):
            database.saveDict("dictionar.txt")
            break
    #print(pytesseract.image_to_string(
    #    r'C:\Users\Liviu.LIVIU-PC.000\Desktop\bot\snap__1603558076.png'))

if __name__ == "__main__"   :
    main()

# play again: 91 -5
