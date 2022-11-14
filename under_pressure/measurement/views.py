from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import sqlite3
from .models import User, Temperature, Humidity, Pressure1, Pressure2

def index(request):

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
    pass

def humidity(request):
    pass

def pressure(request):
    pass

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
    return HttpResponseRedirect(reverse("index"))


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
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "measurement/register.html")
