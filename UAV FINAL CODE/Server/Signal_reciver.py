# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 10:44:49 2023

@author: admin
"""

import socket
import Servo
import serial

#servos and BLDC
BLDC = 12
ELV  = 16
RUD  = 18
ALI  = 22
pin = 0
#GPS on tx-ttyAMA0 or serial0 (8, 10)
ser = serial.Serial("/dev/ttyAMA0" ,baudrate=9600)

def read_GPS():
  GPS = ser.readline().decode().strip()
  #returns a string Time, date, lat, long, speed, course
  return GPS
# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = "pitunnel.com"

# specify port number
port = 12345

# bind the socket to a specific address and port
s.bind((host, port))

# listen for incoming connections
s.listen(1)

print('Waiting for incoming connection...')

# accept the connection from the client
conn, addr = s.accept()

print('Connection from:', addr)

while True:
    signal =s.recv(1024).decode().split(",")
    Angle = signal[1]
    # Send data to the server
    gps = read_GPS()
    
    if gps != None:
        s.send(gps.encode("utf-8"))
    gps = gps.split(",")
    
    if signal[0]=="s1":
        pin = BLDC
    elif signal[0]=="s2":
        pin = ALI
    elif signal[0]=="s3":
        pin = ELV
    elif signal[0]=="s4":
        pin = RUD
        
    Servo.SetAngle(Angle, pin)

# Close the network connection and destroy the window
s.close()
