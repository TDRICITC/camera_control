# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 21:55:51 2021

@author: GWJIANG
"""

import psutil
import os
import time


i = 0
os.chdir(r"C:\Users\GWJIANG\focus_recognition")
for proc in psutil.process_iter():

    if 'camera1' in proc.name():
        print('ok')
        i = i+1
    
    if i==0:
        os.system("camera1_focus.exe")
    
time.sleep(10)       

