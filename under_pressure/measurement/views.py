from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import sqlite3
from json import dumps
from .models import User, Temperature, Humidity, Pressure1, Pressure2

def index(request):
    #Create the default value for Pu risk
    risk_PU = False
    
    #current user
    current_user = request.user

    #Take the data from model table in databse
    lastest_temperature_object = Temperature.objects.filter(user_temperature = current_user.id).order_by('-id').first()
    lastest_temperature = lastest_temperature_object.value
    risk_PU_temperature = lastest_temperature_object.risk_PU
    real_time = lastest_temperature_object.time
    if risk_PU_temperature == True:
        risk_PU = True 
    
    lastest_humidity_object = Humidity.objects.filter(user_humidity = current_user.id).order_by('-id').first()
    lastest_humidity = lastest_humidity_object.value
    risk_PU_humidity = lastest_humidity_object.risk_PU
    if risk_PU_humidity == True:
        risk_PU = True

    lastest_pressure1_object = Pressure1.objects.filter(user_pressure1 = current_user.id).order_by('-id').first()
    lastest_pressure1 = lastest_pressure1_object.pressure_value
    lastest_Tp_pressure1 = lastest_pressure1_object.Tp_value
    risk_PU_pressure1 = lastest_pressure1_object.risk_PU
    if risk_PU_pressure1 == True:
        risk_PU = True


    lastest_pressure2_object = Pressure2.objects.filter(user_pressure2 = current_user.id).order_by('-id').first()
    lastest_pressure2 = lastest_pressure2_object.pressure_value
    lastest_Tp_pressure2 = lastest_pressure2_object.Tp_value
    risk_PU_pressure2 = lastest_pressure2_object.risk_PU
    if risk_PU_pressure2 == True:
        risk_PU = True
   
    return render (request, "measurement/index.html",{
        "lastest_temperature": lastest_temperature,
        "latest_humidity": lastest_humidity,
        "latest_pressure1": lastest_pressure1,
        "lastest_Tp_pressure1": lastest_Tp_pressure1,
        "latest_pressure2": lastest_pressure2,
        "lastest_Tp_pressure2": lastest_Tp_pressure2,
        "risk_PU": risk_PU,
        "real_time": real_time
    })
def temperature(request):
    #current user
    current_user = request.user

    #Find all temperature data related to user 
    temperature_objects = Temperature.objects.filter(user_temperature = current_user.id)

    #JSON data for Javascript pass (value)
    list_temperature_value = []
    for object in temperature_objects:
        list_temperature_value.append(object.value)

    dict_temperature_value = {}
    
    for i in range(len(list_temperature_value)):
        dict_temperature_value[i] = list_temperature_value[i]

    dataJSON = dumps(dict_temperature_value)

    return render(request, "measurement/temperature.html", {
        "temperature_objects": temperature_objects,
        "dataJSON": dataJSON
    })

def humidity(request):
    #current user
    current_user = request.user

    #Find all humidity data related to user 
    humidity_objects = Humidity.objects.filter(user_humidity = current_user.id)

    list_humidity_value = []
    for object in humidity_objects:
        list_humidity_value.append(object.value)

    dict_humidity_value = {}
    
    for i in range(len(list_humidity_value)):
        dict_humidity_value[i] = list_humidity_value[i]

    dataJSON = dumps(dict_humidity_value)

    return render(request, "measurement/humidity.html", {
        "humidity_objects": humidity_objects,
        "dataJSON": dataJSON
    })

def pressure1(request):
    #current user
    current_user = request.user

    #Find all humidity data related to user 
    pressure1_objects = Pressure1.objects.filter(user_pressure1 = current_user.id)

    list_pressure1_value = []
    for object in pressure1_objects:
        list_pressure1_value.append(object.pressure_value)

    dict_pressure1_value = {}
    
    for i in range(len(list_pressure1_value)):
        dict_pressure1_value[i] = list_pressure1_value[i]

    dataJSON = dumps(dict_pressure1_value)

    return render(request, "measurement/pressure1.html", {
        "pressure1_objects": pressure1_objects,
        "dataJSON": dataJSON
    })

def pressure2(request):
    #current user
    current_user = request.user

    #Find all humidity data related to user 
    pressure2_objects = Pressure2.objects.filter(user_pressure2 = current_user.id)

    list_pressure2_value = []
    for object in pressure2_objects:
        list_pressure2_value.append(object.pressure_value)

    dict_pressure2_value = {}
    
    for i in range(len(list_pressure2_value)):
        dict_pressure2_value[i] = list_pressure2_value[i]

    dataJSON = dumps(dict_pressure2_value)

    return render(request, "measurement/pressure2.html", {
        "pressure2_objects": pressure2_objects,
        "dataJSON": dataJSON
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "measurement/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "measurement/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "measurement/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "measurement/register.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "measurement/register.html")