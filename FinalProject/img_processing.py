#!usr/bin/env python3
#####################################################################
### Created by Megan Jenney
### Last Edited 13 April 2022
### 
### Intro to Robotics and Mechanics
### Tufts University Spring 2022
### Department of Mechanical Engineering
### Megan Jenney and Jennifer Liu
###
### Final Project: Robot Cake Baker
### Image Processing Team
### This script processes an image uploaded through Airtable, scales
###     it to the correct shape for the cake, and processes contour
###     lines along which frosting will be dispensed.
#####################################################################

import numpy as np
import cv2
import airtable
import requests
import json
import urllib.request

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

def getContours(image, bg):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,30,200)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def sendToAPI(array_coords, base_id, ctrl_table, api_key):
    at = airtable.Airtable(base_key, table_name, api_key)
    
    record = at.match("Name", "coordinates")
    fields = {'Status': True}
    at.update(record["id"], fields)
    print('sent coords to api')


# get image
base_id = 'appuhn9X6CJyPGaho'
img_table = 'image'
ctrl_table = 'control'
api_key = 'keyxxxxxxxxxxxxxx'
headers = {"Authorization": "Bearer " + api_key}

query = "sort%5B0%5D%5Bfield%5D=Created"
url = "https://api.airtable.com/v0/" + base_id + "/" +img_table + "?" + query

params = ()
response = requests.get(url, params=params, headers=headers)
airtable_response = response.json()

image_url = airtable_response["records"][len(airtable_response["records"])-1]["fields"]["Image"][0]["url"]
#print(image_url)
img = urllib.request.urlretrieve(image_url)

# make binary and resize image
thresh, binary_img = cv2.threshold(img, 136, 255, cv.THRESH_BINARY)
rows = np.shape(binary_img)[0]
cols = np.shape(binary_img)[1]
coord_size = 0.05
resized_img = changeImgRatio(rows,cols,binary_img).astype('uint8')


# get contours and coordinates
#blank = np.zeros(image.shape, dtype='uint8')
contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#contours = cv.findContours(resized_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
list_coords = []
for line in contours[0]:
    for wrapped_point in line:
        list_coords.append(wrapped_point[0])

array_coords = np.asarray(line_coords)
np.savetxt("coordinates.csv", array_coords, delimiter=',')

# export coordinates
#sendToAPI(coords)
