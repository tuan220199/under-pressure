from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import sqlite3
 
def index(request):
    #Take the data from sqlite3 database
    db = sqlite3.connect("mydatabase.db")
    data = db.execute("SELECT * FROM sensors")
    data = data.fetchall()
    number_data = len(data)
    number_group_data = number_data//30

    #Average every 30 chucks of data 
    list_average30_humidity_sensor1 = []
    list_average30_temperature_sensor1 = []
    list_average30_pressure_sensor1 = []
    list_average30_pressure_sensor2 = []

    def avergae_list(list_item):
        return sum(list_item)/len(list_item)

    count = 0
    for i in range(number_group_data):
        list_humidity_sensor1 = []
        list_temperature_sensor1 = []
        list_pressure_sensor1 = []
        list_pressure_sensor2 = []

        data1 = db.execute("SELECT * FROM sensors WHERE id BETWEEN ? AND ?", (i*30,(i+1)*30,))
        data1 = data1.fetchall()
        for item in data1:
            list_humidity_sensor1.append(item[2])
            list_temperature_sensor1.append(item[3])
            list_pressure_sensor1.append(item[4])
            list_pressure_sensor2.append(item[5])
    
        humidity1 = avergae_list(list_humidity_sensor1)
        list_average30_humidity_sensor1.append(humidity1)
        temperature1 =avergae_list(list_temperature_sensor1)
        list_average30_temperature_sensor1.append(temperature1)
        pressure1 = avergae_list(list_pressure_sensor1)
        list_average30_pressure_sensor1.append(pressure1)
        pressure2 = avergae_list(list_pressure_sensor2)
        list_average30_pressure_sensor2.append(pressure2)

    average_total_humidity = avergae_list(list_average30_humidity_sensor1)
    average_total_temperature = avergae_list(list_average30_temperature_sensor1)
    average_total_pressure_sensor1 = avergae_list(list_average30_pressure_sensor1)
    average_total_pressure_sensor2 = avergae_list(list_average30_pressure_sensor2)
    
    return render (request, "measurement/index.html",{
        "average_total_humidity": average_total_humidity,
        "average_total_temperature": average_total_temperature,
        "average_total_pressure_sensor1": average_total_pressure_sensor1,
        "average_total_pressure_sensor2": average_total_pressure_sensor2,
        "list_average30_humidity_sensor1": list_average30_humidity_sensor1,
        "list_average30_temperature_sensor1": list_average30_temperature_sensor1,
        "list_average30_pressure_sensor1": list_average30_pressure_sensor1,
        "list_average30_pressure_sensor2": list_average30_pressure_sensor2
    })
# Create your views here.
