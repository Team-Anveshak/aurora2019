#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 16:39:10 2018

@author: Tanay Dwivedi
"""
import cv2
import time

# Video Stream
cap = cv2.VideoCapture(1)

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

print(start_time)

while True:
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    
    start_time = time.localtime();
    start_time = time.mktime(start_time)
    
    if start_time > start_time_2:
        cv2.imwrite('images/'+ str(i) +'.jpg',frame)
        start_time_2 = start_time_2 + t_interval
        i = i + 1
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
