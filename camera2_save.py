# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 11:09:39 2021

@author: GWJIANG
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 15:24:41 2021

@author: GWJIANG
"""

import cv2
import mediapipe as mp
import time
from cvzone.PoseModule import PoseDetector
from datetime import datetime
import requests
import json
import os





develope_mode = True


print('open cam ...')
cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

print('success open cam ...')

user = '0'
user_switch = 0
i = -1


date = datetime.now().strftime('%Y-%m-%d')
detector = PoseDetector()
os.getcwd()

save_path = './image2/'+date
if not os.path.exists(save_path):
    os.makedirs(save_path)
os.chdir(save_path)


while cap.isOpened():
    i = i+1
    success, image = cap.read()

    ###########################################################################################
    if i%30 == 0 and user == '1':
        now = datetime.now().strftime('%Y%m%d-%H%M%S')
        cv2.imwrite(now+'.jpg', image)
        print("save image-"+now)
        
    ###########################################################################################
    image = detector.findPose(image)
    lmList, bboxInfo = detector.findPosition(image, bboxWithHands=False)
   

    if  bboxInfo and user == '0':
        user = '1'
        
    elif not bboxInfo and user == '1':
        user = '0'


    ###########################################################################################
    
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    ###########################################################################################
    
    if cv2.waitKey(1) & 0xFF == 27:
        break
    
    cv2.imshow('MediaPipe Face Mesh', image)
    
cap.release()
cv2.destroyAllWindows() 
