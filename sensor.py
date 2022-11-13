import time
import serial
import datetime
import numpy
import matplotlib.pyplot as plt
from drawnow import *
import sqlite3

def main():
    # Create the baudrate and serial com
    arduinoData = serial.Serial("COM4", 9600)
    time.sleep(1)

    # Create series of lists for measurements
    list_humidity_sensor1 = []
    list_temperature_sensor1 = []
    list_pressure_sensor1 = []
    list_pressure_sensor2 = []
    time_frame = []

    # Set up the database with sqlite 3
    db = sqlite3.connect("under_pressure/mydatabase.db")

    # Forever loop to receive and process data
    while True:
        # Check if the arduino and computer is connected or not
        while (arduinoData.inWaiting()==0):
            pass

        # Read the data transmited from Arduino as string
        data_receive_Arduino = arduinoData.readline()
        data_receive_Arduino = str(data_receive_Arduino,"utf-8")
        
        # Convert string data into list of all measurement: Temp, Hud, Pressure
        data_list = data_receive_Arduino.split(",")

        # Check if the data has full 4 measurements or not
        if (len(data_list) != 4):
            continue
        else:
            humidity_sensor1 = float(data_list[0])
            temperature_sensor1 = float(data_list[1])
            pressure_sensor1 = float(data_list[2])
            pressure_sensor2 = float(data_list[3])

        # Take the real time data when data is received 
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_frame.append(now)

        # Insert valid data into sensors table 
        db.execute("INSERT INTO sensors (time, humidity1, temperature1, pressure1, pressure2) values (?, ?, ?, ?, ?)",(now, humidity_sensor1, temperature_sensor1, pressure_sensor1, pressure_sensor2))
        db.commit()
        # Append new measurement into list
        list_humidity_sensor1.append(humidity_sensor1)
        list_temperature_sensor1.append(temperature_sensor1)
        list_pressure_sensor1.append(pressure_sensor1)
        list_pressure_sensor2.append(pressure_sensor2)
