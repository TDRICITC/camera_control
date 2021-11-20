# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 21:55:51 2021

@author: GWJIANG
"""

import psutil
import os
import time


i1 = 0
i2 = 0
i3 = 0
i4 = 0
os.chdir(r"C:\Users\GWJIANG\focus_recognition")

for proc in psutil.process_iter():

    if 'camera1' in proc.name():
        print('camera1_ok')
        i1 = i1+1
    if i1==0:
        os.system("camera1_focus.exe")
        print('camera1_restart')
    if 'camera2' in proc.name():
        print('camera2_ok')
        i2 = i2+1
    if i2==0:
        os.system("camera2_focus.exe")  
        print('camera2_restart')
    if 'camera3' in proc.name():
        print('camera3_ok')
        i3 = i3+1
    if i3==0:
        os.system("camera3_focus.exe")  
        print('camera3_restart')
    if 'camera4' in proc.name():
        print('camera4_ok')
        i4 = i4+1
    if i4==0:
        os.system("camera4_focus.exe") 
        print('camera4_restart')
        
time.sleep(600) 
