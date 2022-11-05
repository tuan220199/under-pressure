import time
import serial
import datetime
import numpy
import matplotlib.pyplot as plt
from drawnow import *
import sqlite3

def main():
    # Create the baudrate and serial com
    arduinoData = serial.Serial("com4", 9600)
    time.sleep(1)

    # Create series of lists for measurements
    list_humidity_sensor1 = []
    list_temperature_sensor1 = []
    list_pressure_sensor1 = []
    list_pressure_sensor2 = []
    time_frame = []

    # Turn on live mode to plot data live 
    plt.ion()

    # Set up the database with sqlite 3
    db = sqlite3.connect("mydatabase.db")
    
    # Variable cnt to count number of points in graph 
    cnt = 0
    
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

        
        def makeFig():
            #figure = plt.subplots(3,2)
            #figure.tight_layout(pad =0.5)
            plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

            # Humidity of sensor 1 graph 
            ax1 = plt.subplot(3,2,1)
            ax1.set_title("Humidity sensor 1")
            ax1.set_ylabel("Humidity [%RH]")
            ax1.set_ylim([0,100])
            ax1.plot(list_humidity_sensor1,'ro-')
            
            # Temperature of sensor 1 graph
            ax2 = plt.subplot(3,2,3)
            ax2.set_title("Temperature sensor 1")
            ax2.set_ylabel("Temperature [oC]")
            ax2.set_ylim([0,40])
            ax2.plot(list_temperature_sensor1,'go-')
            
            # Pressure of sensor 1 graph
            ax3 = plt.subplot(3,2,5)
            ax3.set_title("Pressure sensor 1")
            ax3.set_ylabel("Pressure [mmHg]")
            ax3.set_ylim([0,5])
            ax3.plot(list_pressure_sensor1,'bo-')
            
            # Pressure of sensor 2 graph 
            ax4 = plt.subplot(3,2,6)
            ax4.set_title("Pressure sensor 2")
            ax4.set_ylabel("Pressure [mmHg]")
            ax4.set_ylim([0,5])
            ax4.plot(list_pressure_sensor2,'co-')

        #Call draw on to update list
        drawnow(makeFig)
        plt.pause(0.000001)

        #If the number of points larger than 10 points, it will drop the first item in list (first point)
        # => reamin 10 points in the graph  
        cnt = cnt + 1
        if (cnt>10):
            list_humidity_sensor1.pop(0)
            list_temperature_sensor1.pop(0)
            list_pressure_sensor1.pop(0)
            list_pressure_sensor2.pop(0)

        time.sleep(1)
        #print(f"{now},{humidity_sensor1},{temperature_sensor1},{pressure_sensor1},{pressure_sensor2}")



if __name__ == "__main__":
    main()