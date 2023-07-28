''' Creo le mie funzoni per i miei template'''
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import get_template
from django.template import Context

from django.shortcuts import render, redirect
from django.views.generic import CreateView
import bcrypt
from .models import *
from .forms import *
from .functions import *
from DjangoWebApp.settings import DATABASES

class CreatePerson(CreateView):
    model = UserRegisterForm
    template_name = 'register.html'
    fields = ['username', 'email', 'fullname', 'age', 'gender', 'password']

global_username = ""

# Create your views here.
def index(request):
    if request.user.myblog_user:
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
            return redirect('index')
        else:
            error = True
            return redirect('login', {'error': error})
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

############## register function ###############
def register(request):
    error = False # compare quando l'email è già in uso
    req_psw = False #compare se non vengono soddisfatti i requisiti minimi

    if request.method == "POST":
        form_data = request.POST
        #Purtroppo recupera solamente il form senza i dati 
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            #recupero dati dal UserRegistrationForm
            username = form_data['username']
            email = form_data['email']
            fullname = form_data['fullname']
            age = form_data['age']
            gender = form_data['gender']
            email = form_data['email']
            password1 = form_data['password1']

            #procedimento per heshare la password
            not_hashed_psw = password1
            password1 = password1.encode('utf-8')
            hashed_psw = bcrypt.hashpw(password1, bcrypt.gensalt())
            
            
            if check_email_exist(email):
                error = True
                return render(request, "register.html", {'error': error})
            
            
            #Check della password, con Django non è necessario fare un controllo
            #inutile per le password che metchano, lo fa in automatico
            if requirements_pass(not_hashed_psw):
                #salvo il form  in DB  
                form.save()
                return redirect('login')
            else:
                req_psw = True
                return render(request, "register.html", {'form': form, 'req_psw': req_psw})
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def logout(request):
    return render(request, "index.html")

def recovery(request):
    return render(request, "recovery.html")
