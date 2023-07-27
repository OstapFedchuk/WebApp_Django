''' Creo le mie funzoni per i miei template'''

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.template.loader import get_template
from django.template import Context
import bcrypt
from .models import User, Contact


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

#register function
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
    return render(request, "register.html")

def logout(request):
    return render(request, "index.html")

def recovery(request):
    return render(request, "recovery.html")
