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


def logAPI(log):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    requests.post("http://34.81.45.156/venapis/log", data=log, headers=headers)


mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

develope_mode = True

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
print('open cam ...')
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = PoseDetector()
print('success open cam ...')

l=[]
watch_where  = 'No Looking'
state = 'focus'
user = '0'
continue_watch = 0
no_watch_time = 0.0001
user_switch = 0
response = ''
uid = 0
i = -1
j=5


date = datetime.now().strftime('%Y-%m-%d')

os.getcwd()

save_path = './image/'+date
if not os.path.exists(save_path):
    os.makedirs(save_path)

os.chdir(save_path)


with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        i = i+1
        success, image = cap.read()

        ###########################################################################################
        if i%30 == 0 and user == '1':
            now = datetime.now().strftime('%Y%m%d-%H%M%S')
            cv2.imwrite(now+'.jpg', image)
        ###########################################################################################
        image = detector.findPose(image)
        lmList, bboxInfo = detector.findPosition(image, bboxWithHands=False)
       
        if i%10 == 0:
            if  bboxInfo and user == '0':
                
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                uid = time.time()
                uid = str(round(uid))
                d = {
                    "uid":uid, 
                    "action":"user_in",
                    "device":"pc",
                    "timestamp": now
                }
                log = {'user_in': json.dumps(d)}
                logAPI(log)
                user = '1'
            
        if bboxInfo:
            center = bboxInfo["center"]
            cv2.circle(image, center, 5, (255, 0, 255), cv2.FILLED)
        
        elif not bboxInfo and user == '1':
            user = '0'
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            d = {
                    "uid":uid, 
                    "action":"user_out",
                    "device":"pc",
                    "timestamp": now
                }
            log = {'user_out': json.dumps(d)}
            logAPI(log)
            
        #print(user)

        ###########################################################################################
        
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_face_landmarks:
            landmark_z_list = [results.multi_face_landmarks[0].landmark[zz].z for zz in range(468)]
            landmark_x_list = [results.multi_face_landmarks[0].landmark[xx].x for xx in range(468)]

            forehead_relative = landmark_z_list[151]-landmark_z_list[0]
            check_relative = landmark_z_list[175]-landmark_z_list[0]
            vertical_diff = forehead_relative-check_relative
            max_vertical_diff = abs(max(landmark_z_list) - min(landmark_z_list))
            nor_vertical_diff = vertical_diff/max_vertical_diff
            nose = landmark_x_list[1]
            right_cheek = landmark_x_list[93]
            left_cheek = landmark_x_list[323]
            right_cheek_diff = abs(right_cheek-nose)/abs(max(landmark_x_list)-min(landmark_x_list))
            left_cheek_diff = abs(left_cheek-nose)/abs(max(landmark_x_list)-min(landmark_x_list))

            # recongnition
            up_thres = 0.4
            down_thres = -0.45
            left_thres = 0.75
            right_thres = 0.75
            state = 'focus'
            if right_cheek_diff>left_thres:
                state = 'left'
            elif left_cheek_diff>right_thres:
                state = 'right'
            elif nor_vertical_diff<down_thres:
                state = 'down'
            elif nor_vertical_diff>up_thres:
                state = 'up'

            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks)
            # Flip the image horizontally for a selfie-view display.
            result_img = cv2.flip(image, 1)
            if develope_mode:
                result_img = cv2.putText(result_img, 'user:'+user, (10, 60), cv2.FONT_HERSHEY_PLAIN,1, (0, 0, 255), 1, cv2.LINE_AA)
                result_img = cv2.putText(result_img, 'up & down:'+'%.3f'%nor_vertical_diff, (10, 80), cv2.FONT_HERSHEY_PLAIN,1, (0, 0, 255), 1, cv2.LINE_AA)
                result_img = cv2.putText(result_img, 'left:'+'%.3f'%right_cheek_diff, (10, 100), cv2.FONT_HERSHEY_PLAIN,1, (0, 0, 255), 1, cv2.LINE_AA)
                result_img = cv2.putText(result_img, 'right:'+'%.3f'%left_cheek_diff, (10, 120), cv2.FONT_HERSHEY_PLAIN,1, (0, 0, 255), 1, cv2.LINE_AA)
                result_img = cv2.putText(result_img, watch_where, (10, 30), cv2.FONT_HERSHEY_DUPLEX,1, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.imshow('MediaPipe Face Mesh', result_img)
            #result_img = cv2.putText(result_img, state, (10, 30), cv2.FONT_HERSHEY_DUPLEX,1, (0, 0, 255), 1, cv2.LINE_AA)
            
            
        else:
            if develope_mode:
                image = cv2.flip(image, 1)
                image = cv2.putText(image, 'user:'+user, (10, 60), cv2.FONT_HERSHEY_PLAIN,1, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.imshow('MediaPipe Face Mesh',image)
        
        #time.sleep(0.1)
        if len(l) >= 10:
            l.pop(0)
            l.append(state)
            if l.count('focus')>8:
                watch_where  = 'Looking'
            else:
                watch_where  = 'No Looking'
        else:
            l.append(state)
            if l.count('focus')>=8:
                watch_where  = 'Looking'
            else:
                watch_where  = 'loading'
                
        ###########################################################################################
        
        if watch_where == "No Looking" and continue_watch == 0:
            no_watch_start = time.time()
            continue_watch = 1
        elif watch_where == "No Looking" and continue_watch == 1:  
            no_watch_end = time.time()
            no_watch_time = no_watch_end - no_watch_start
        elif watch_where == "Looking":
            continue_watch = 0
            response = ''
        #print (no_watch_time)
        #print(j)
       #發出警告
        
        if user == '1' and no_watch_time / j > 1:
           
            print('in')
            j = j+5
            response = 'warning'
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            d = {
                    "uid":uid, 
                    "action":"warning",
                    "device":"pc",
                    "timestamp": now
                }
            log = {'warning': json.dumps(d)}
            logAPI(log)
            
        
        ###########################################################################################
        

        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows() 
