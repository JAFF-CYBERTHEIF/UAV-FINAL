# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 16:35:20 2023

@author: admin
"""
import controller
import socket
import csv


# Set up the network socket
HOST = 'pitunnel.com'  # Replace with HOST address
PORT = 45004
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

with open('sensor_data.csv', mode='w', newline='') as file:

    # Create a CSV writer object
    writer = csv.writer(file)

    # Write a header row with column names
    writer.writerow(['Time', 'Date', 'LAT', 'LONG', 'Speed', 'Course'])
    while True:

        # Send data to the server
        message = controller.get_signal()
        
        if message != None:
            print("msg ",message)
            s.send(message.encode("utf-8"))
        data =s.recv(1024).decode()
        data = data.split(",")
        writer.writerow(data)
# Close the network connection and destroy the window
s.close()
