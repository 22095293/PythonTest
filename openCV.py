# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 15:57:20 2022

@author: stein
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np


def get_edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (13,13), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def get_roi(img): 
    mask = np.zeros_like(img)
    points = np.array([[[146, 539], [781, 539], [515, 417], [296, 397]]])
    cv2.fillPoly(mask, points, 255)
    roi = cv2.bitwise_and(img, mask)
    return roi

def draw_line(img, lines):
    for line in lines:
        points = line.reshape(4, )
        x1, y1, x2, y2 = points
        cv2.line(img, (x1, y1), (x2, y2), (0,0,255), 3)
    return img

def get_avglines(lines):
    if lines is None:
        print('偵測不到直線線段')
        return None
    lefts = []
    rights = []
    
    for line in lines:
        points = line.reshape(4, )
        x1, y1, x2, y2 = points
        slope, b = np.polyfit((x1, x2), (y1, y2), 1)
        
        if slope > 0:
            rights.append([slope, b])
        else:
            lefts.append([slope, b])
    
    if rights and lefts:
        right_avg = np.average(rights, axis=0)
        left_avg = np.average(lefts, axis=0)
        return np.array([right_avg, left_avg])
    else:
        print("failt")
        return None
        
def get_sublines(img, avglines):
    sublines = []
    for line in avglines:
        slope, b = line
        y1 = img.shape[0]
        y2 = int(y1*(3/5))
        x1 = int((y1-b) / slope)
        x2 = int((y2-b) / slope)
        sublines.append([x1, y1, x2, y2])
    return np.array(sublines)
    
img = cv2.imread("C:\\Users\\stein\\OneDrive\\road.jpg")

edge = get_edge(img)

roi = get_roi(edge)

lines = cv2.HoughLinesP(image=roi, rho=3, theta = np.pi/180, threshold=60,
                        minLineLength=40, maxLineGap=50)

avglines = get_avglines(lines)

if avglines is not None:
    lines = get_sublines(img, avglines)    
    img = draw_line(img, lines)
    cv2.imshow("Edge", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
#plt.imshow(edge)
#plt.show()


