#!usr/bin/env python3
### Created by Megan Jenney
### Last Edited 25 March 2022
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

import numpy as np
import cv2 as cv

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


img = cv.imread("trees_allcontours.jpeg", cv.IMREAD_REDUCED_GRAYSCALE_2)

thresh, bin_img = cv.threshold(img, 136, 255, cv.THRESH_BINARY)

print(np.shape(bin_img))

rows = np.shape(bin_img)[0]
cols = np.shape(bin_img)[1]

pan_ratio = 9/13
img_ratio = rows / cols

print(pan_ratio)
print(img_ratio)

if img_ratio < pan_ratio:
    print("add rows")
    add_top, add_btm = rowsToAdd(cols, rows)
    new_img = addRows(add_top, add_btm, bin_img)
        
elif img_ratio > pan_ratio:
    print("add columns")
    add_lft, add_rgt = colsToAdd(rows, cols)
    new_img = addCols(add_lft, add_rgt, bin_img)
else:
    print("dont add")
    new_img = bin_img


cv.imwrite("modified_image.jpeg", new_img)
