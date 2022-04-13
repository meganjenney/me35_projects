#!usr/bin/env python3
### Created by Megan Jenney
### Last Edited 12 April 2022
### 
### Intro to Robotics and Mechanics
### Tufts University Spring 2022
### Department of Mechanical Engineering
###
### Final Project: Robot Cake Baker
### Image Processing
### This script tests image processing methods for the image
###     processing team. Focus on translation from binary contour
###     image to coordinates, which will be sent to the frosting
###     mechanism team.
### Each coordinate is equivalent to a square of 0.05in x 0.05in.
### Coordinates are sent as a list in gcode (x,y,e) format.
#####################################################################

import numpy as np
import cv2 as cv
import airtable
import pandas as pd
from matplotlib import pyplot

# function definitions
def rowsToAdd(pix_col, pix_row):
    in_pix_ratio = pix_col / 13
    corr_rows = in_pix_ratio * 9
    add_rows = abs(int(corr_rows) - pix_row)
    
    if not add_rows % 2 == 0:
        add_top = int(add_rows / 2 + 0.5)
        add_btm = int(add_rows / 2 - 0.5)
    else:
        add_top = int(add_rows / 2)
        add_btm = int(add_rows / 2)
    
    return (add_top, add_btm)

def colsToAdd(pix_row, pix_col):
    in_pix_ratio = pix_row / 9
    corr_cols = in_pix_ratio * 13
    add_cols = abs(int(corr_cols) - pix_col)
    
    if not add_cols % 2 == 0:
        add_lft = int(add_cols / 2 + 0.5)
        add_rgt = int(add_cols / 2 - 0.5)
    else:
        add_lft = int(add_cols / 2)
        add_rgt = int(add_cols / 2)
    
    return (add_lft, add_rgt)

def addRows(add_top, add_btm, img):
    pix_col = np.shape(img)[1]
    
    top_shape = (add_top, pix_col)
    top = np.full(top_shape, 0)
    btm_shape = (add_btm, pix_col)
    btm = np.full(btm_shape, 0)
    
    return np.concatenate((top, img, btm))

def addCols(add_left, add_rgt, img):
    pix_row = np.shape(img)[0]
    
    lft_shape = (pix_row, add_lft)
    lft = np.full(lft_shape, 0)
    rgt_shape = (pix_row, add_rgt)
    rgt = np.full(rgt_shape, 0)
    
    return np.concatenate((lft, img, rgt), axis=1)

def changeImgRatio(rows, cols, img):
    pan_ratio = 6 / 7.5
    img_ratio = rows / cols

    if img_ratio < pan_ratio:
        add_top, add_btm = rowsToAdd(cols, rows)
        return addRows(add_top, add_btm, img)
        
    elif img_ratio > pan_ratio:
        add_lft, add_rgt = colsToAdd(rows, cols)
        return addCols(add_lft, add_rgt, bin_img)
    else:
        return img

def changeImgScale(coord_size, img):
    dims = (int(7.5 / coord_size), int(6 / coord_size))
    float_img = img.astype('float32')
    return cv.resize(float_img, dims, interpolation=cv.INTER_AREA)

def resizeImg(rows, cols, coord_size, img):
    ratio_img = changeImgRatio(rows, cols, img)
    return changeImgScale(coord_size, ratio_img)

def coordList(coord_size, img):
    coords = []
    for x in range(int(6 / coord_size)):
        for y in range(int(7.5 / coord_size)):
            e = img[x,y]
            if e == 0.0:
                coords.append([x,y,0])
            else:
                coords.append([x,y,1])
    return coords

def sendToAPI(coords):
    base_key = 'appuhn9X6CJyPGaho'
    table_name = 'control'
    api_key = 'keylvkrPfqTyKrObK'
    at = airtable.Airtable(base_key, table_name, api_key)
    
    record = at.match("Name", "coordinates")
    fields = {'Status': True}#, 'Attachment': coords}
    at.update(record["id"], fields)
    print('sent coords to api')
    

# import image
img = cv.imread("trees_allcontours.jpeg", cv.IMREAD_GRAYSCALE)

thresh, binary_img = cv.threshold(img, 136, 255, cv.THRESH_BINARY)


rows = np.shape(binary_img)[0]
cols = np.shape(binary_img)[1]
coord_size = 0.05
resized_img = changeImgRatio(rows,cols,binary_img).astype('uint8')
#scaled_img = resizeImg(rows, cols, coord_size, binary_img).astype('uint8')
#print(np.shape(resized_img))
# export image to new file
cv.imwrite("resized_image.jpeg", resized_img)
#print(cv.imread('scaled_image.jpeg', cv.IMREAD_GRAYSCALE).dtype)


contours = cv.findContours(resized_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
line_coords = []
for line in contours[0]:
    for wrapped_point in line:
        line_coords.append(wrapped_point[0])

#pyplot.figure()
#pyplot.scatter(line_coords[:][0], line_coords[:][1])
#pyplot.show()
array_coords = np.asarray(line_coords)
np.savetxt("coordinates.csv", array_coords, delimiter=',')
#np.savetxt("coords.csv", a, delimiter=',')
# export coordinates
#sendToAPI(coords)
