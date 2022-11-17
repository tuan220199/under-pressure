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
    db = sqlite3.connect("under_pressure/db.sqlite3")

    #Create threshold values for Temperature, Humidity, Pressure
    temperature_threshold = 37
    humidity_threshold = 70 
    pressure_threshold = 32
    Tp1 = 0
    Tp2 = 0

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

        # Append new measurement into list
        list_humidity_sensor1.append(humidity_sensor1)
        list_temperature_sensor1.append(temperature_sensor1)
        list_pressure_sensor1.append(pressure_sensor1)
        list_pressure_sensor2.append(pressure_sensor2)

        # Calculate the avaerage value of measurement every 5 minutes = 5*4(4 measurement per 15 seconds) = 20)
        if len(list_humidity_sensor1)==8:
            average_5_min_humidity = average_list(list_humidity_sensor1)
            average_5_min_temperature = average_list(list_temperature_sensor1)
            average_5_min_pressure1 = average_list(list_pressure_sensor1)
            average_5_min_pressure2 = average_list(list_pressure_sensor2)

            if average_5_min_temperature > temperature_threshold:
                PU_risk = True
                db.execute("INSERT INTO measurement_temperature (value, time, risk_PU, user_temperature_id) values (?, ?, ?, ?)",( average_5_min_temperature, now, PU_risk, 2))
                db.commit()
            else:
                PU_risk = False
                db.execute("INSERT INTO measurement_temperature (value, time, risk_PU, user_temperature_id) values (?, ?, ?, ?)",(average_5_min_temperature, now, PU_risk, 2))
                db.commit()         

            if average_5_min_humidity > humidity_threshold:
                PU_risk = True
                db.execute("INSERT INTO measurement_humidity (value, time, risk_PU, user_humidity_id) values (?, ?, ?, ?)",(average_5_min_humidity, now, PU_risk, 2))
                db.commit()
            else:
                PU_risk = False
                db.execute("INSERT INTO measurement_humidity (value, time, risk_PU, user_humidity_id) values (?, ?, ?, ?)",(average_5_min_humidity, now, PU_risk, 2))
                db.commit()
            
            if average_5_min_pressure1> pressure_threshold:
                Tp1 += 5
                if Tp1 >= 60:
                    PU_risk = True
                    db.execute("INSERT INTO measurement_pressure1 (pressure_value, Tp_value, time, risk_PU, user_pressure1_id) values (?, ?, ?, ?, ?)",(average_5_min_pressure1, Tp1, now, PU_risk, 2))
                    db.commit()
                else:
                    PU_risk = False
                    db.execute("INSERT INTO measurement_pressure1 (pressure_value, Tp_value, time, risk_PU, user_pressure1_id) values (?, ?, ?, ?, ?)",(average_5_min_pressure1, Tp1, now, PU_risk, 2))
                    db.commit()
            else:
                PU_risk = False
                db.execute("INSERT INTO measurement_pressure1 (pressure_value, Tp_value, time, risk_PU, user_pressure1_id) values (?, ?, ?, ?, ?)",(average_5_min_pressure1, Tp1, now, PU_risk, 2))
                db.commit()
                Tp1 = 0

            if average_5_min_pressure2> pressure_threshold:
                Tp2 += 5
                if Tp2 >= 60:
                    PU_risk = True
                    db.execute("INSERT INTO measurement_pressure2 (pressure_value, Tp_value, time, risk_PU, user_pressure1_id) values (?, ?, ?, ?, ?)",(average_5_min_pressure2, Tp2, now, PU_risk, 2))
                    db.commit()
                else:
                    PU_risk = False
                    db.execute("INSERT INTO measurement_pressure2 (pressure_value, Tp_value, time, risk_PU, user_pressure1_id) values (?, ?, ?, ?, ?)",(average_5_min_pressure2, Tp2, now, PU_risk, 2))
                    db.commit()
            else:
                PU_risk = False
                db.execute("INSERT INTO measurement_pressure2 (pressure_value, Tp_value, time, risk_PU, user_pressure2_id) values (?, ?, ?, ?, ?)",(average_5_min_pressure2, Tp2, now, PU_risk, 2))
                db.commit()
                Tp2 = 0

            list_humidity_sensor1 = []
            list_temperature_sensor1 = []
            list_pressure_sensor1 = []
            list_pressure_sensor2 = []
            time_frame = []


def average_list(list_data):
    return sum(list_data)/len(list_data)

if __name__ == "__main__":
    main()