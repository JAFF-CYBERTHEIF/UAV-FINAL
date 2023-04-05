# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 10:39:13 2023

@author: admin
"""

import Rpi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)

def SetAngle(angle,pin):
    pwm = GPIO.PWM(pin,50)
    pwm.start(0)
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)
    sleep(0.5)
    pwm.ChangeDutyCycle(0)
