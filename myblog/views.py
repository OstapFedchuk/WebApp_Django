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
from .functions import *

global_username = ""

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        global_username = request.user.username
        return render(request, "index.html", {'global_username': global_username}) 
    else:
        global_username = "Guest"
        return render(request, "index.html", {'global_username': global_username})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def info(request):
    return render(request, "info.html")

def gitstatus(request):
    return render(request, "gitstatus.html")

############## login function ###############
def login(request):
    error = False

    if request.method == 'POST':
        gen_user =  request.POST['gen_user']
        password = request.POST['password']
        user = authenticate(request, gen_user = gen_user, password = password)
        if user is not None:
            form = login(request,user)
            return redirect('index', {'global_username': gen_user})
        else:
            error = True
            return redirect('login', {'error': error})
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

############## register function ###############
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            register_user_to_db(username,email,fullname,age,gender,password)
            form.save()

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            fullname = form.cleaned_data.get('fullname')
            age = form.cleaned_data.get('age')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')

            messages.success(request, f'Your account has been creted')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def logout(request):
    return render(request, "index.html")

def recovery(request):
    return render(request, "recovery.html")
