from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

#from .models import User, 
def index(request):
    return HttpResponse ("Hello, world!")
# Create your views here.
