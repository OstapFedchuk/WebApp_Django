''' Creo le mie funzoni per i miei template'''

from django.shortcuts import render, HttpResponse
import bcrypt
import os
from .models import Signup, Contact
from .functions import *


# Create your views here.
def index(request):
    global_username = "Giovanni"
    return render(request, "index.html", {"global_username": global_username}) #locals()

def about(request):
    global_username = "Giovanni"
    return render(request, "about.html", {"global_username": global_username})

def contact(request):
    global_username = "Giovanni"
    return render(request, "contact.html", {"global_username": global_username})

def info(request):
    global_username = "Giovanni"
    return render(request, "info.html", {"global_username": global_username})

def gitstatus(request):
    return render(request, "gitstatus.html")

def login(request):
    return render(request, "login.html")

def register(request):

    return render(request, "register.html")

def logout(request):
    return render(request, "index.html")

def recovery(request):
    return render(request, "recovery.html")
