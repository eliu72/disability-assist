import numpy as np
import cv2
import random
import math

# running virtual environment on windows
###############################################
# virtualenv env
# .\env\Scripts\activate.bat
# python app.py

# read the image file
img = cv2.imread('maps/atl-2.png', 2)

# convert to binary image
ret, bw_img = cv2.threshold(img, 254, 255, cv2.THRESH_BINARY)

# take a random sample of widths
width = 0
for i in range(100):
    index = random.randint(0,len(bw_img)-1)
    first = np.where(bw_img[index]==255)
    if (first[0].size != 0):
        width += first[0][-1] - first[0][0]

width = math.floor(width / 100)

# perform dilation (width/2) times
kernel = np.ones((3,3), np.uint8)
img_dilation = cv2.dilate(bw_img, kernel, iterations=width*2)
img_erosion = cv2.erode(img_dilation, kernel, iterations=math.floor(width*2))
                
cv2.imshow('Dilation', img_erosion)
cv2.waitKey(0)
cv2.destroyAllWindows()
