# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 16:36:43 2023

@author: admin
"""

import pygame
import math
import time
# initialize pygame
pygame.init()

# initialize joystick
joystick = pygame.joystick.Joystick(1)
joystick.init()

# map button names to indices
button_names = {
    0: "1",
    1: "2",
    2: "3",
    3: "4",
    4: "L1",
    5: "R1",
    6: "L2",
    7: "R2",
    8: "Left Stick",
    9: "START",
    10: "Home",
    11: "DPad"
}


def joystick_info():
    # print some joystick info
    print(f"Joystick Name: {joystick.get_name()}")
    print(f"Number of Buttons: {joystick.get_numbuttons()}")
    print(f"Number of Axes: {joystick.get_numaxes()}")
    print(f"Number of HAT: {joystick.get_numhats()}")

def signal_to_angle(signal):
    Angle = signal * 90
    return Angle

def get_signal():
    button_name = ""
    stick = ""
    HAT =""
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            #button = joystick.get_button(event.button)
            button_name = "b," + button_names.get(event.button, f"Button {event.button}") 
            return button_name
        if event.type == pygame.JOYAXISMOTION:
            axis = joystick.get_axis(event.axis)
            angle = math.floor(signal_to_angle(axis + 1))
            stick = "s" + str(event.axis) + ", " + str(angle) 
            return stick
        if event.type == pygame.JOYHATMOTION:
            hat = joystick.get_hat(event.hat)
            HAT =  "h,"+ str(hat[0]) + "," +  str(hat[1])   
            return HAT

while True:
    print(get_signal())
    time.sleep(0.01)