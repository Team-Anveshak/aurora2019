#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 16:39:10 2018

@author: Tanay Dwivedi
"""
import cv2
import time

# global constants
partition_x = 3
partition_y = 3
image_size = 448

# Video Stream
cap = cv2.VideoCapture('dataset/video5.mp4')

# Image folder
image_folder = 'images'

# Time interval
t_interval = 0.3

# Computer Local Time
start_time = time.localtime();
start_time = time.mktime(start_time)

# Setting a temprorary variable as current time
start_time_2 = start_time
start_time = start_time + t_interval

# Index of images
i = 1

# Function to crop image
print(start_time)

def crop_image(image):
    width, height, col = image.shape
    w_x = (width - image_size) / partition_x
    h_y = (height - image_size) / partition_y
    x_begin = 0
    y_begin = 0
    for j in range(1,partition_x+1):
        for k in range(1,partition_y+1):
            img_crop = image[x_begin:x_begin+image_size , y_begin:y_begin+image_size]
            cv2.imwrite(image_folder + '/' + str(i) + '_' + str(j) + '_' + str(k) + '.jpg',img_crop)
            y_begin = y_begin + h_y
        x_begin = x_begin + w_x
        y_begin = 0

while True:
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    
    start_time = time.localtime();
    start_time = time.mktime(start_time)
    
    if start_time > start_time_2:
        # cv2.imwrite('images/'+ str(i) +'.jpg',frame)
        crop_image(frame)
        start_time_2 = start_time_2 + t_interval
        i = i + 1
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
