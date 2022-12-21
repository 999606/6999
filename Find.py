import time
import numpy as np
import pyscreenshot as ImageGrab
import cv2
import os
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

filename = 'Image.png'
x = 1
last_time = time.time()

while(True):
    screen = np.array(ImageGrab.grab(bbox=(1767, 276, 3050, 1679)))
    #print('loop took {} seconds'.format(time.time()-last_time))
    last_time = time.time()
    cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    cv2.imwrite(filename, screen)
    x = x + 1
    #print(x)
    if x == 2:
        cv2.destroyAllWindows()
        break

img = cv2.imread('Image.png')
text = pytesseract.image_to_string(img, lang='rus')
print(text)