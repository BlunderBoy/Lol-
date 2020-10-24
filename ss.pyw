from PIL import ImageGrab
import os
import time

# Globals
# ------------------

x_pad = 709
y_pad = 359
 
def screenGrab():
    box = (x_pad + 1, y_pad + 1, x_pad + 549, y_pad + 499)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\snap__' + str(int(time.time())) +
'.png', 'PNG')
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()


# x: 710 y: 360
# x: 1260 y: 860
