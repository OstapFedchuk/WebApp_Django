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

class CreatePerson(CreateView):
    model = UserRegisterForm
    template_name = 'register.html'
    fields = ['username', 'email', 'fullname', 'age', 'gender', 'password']

global_username = ""

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        global_username = request.user.is_authenticated
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
        form = UserRegisterForm(form_data) 
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

            #controllo se l'email è già in uso
            if User.objects.filter(email=email).exists():
                error = True
                return render(request, "register.html", {"error": error, "form": form})   
                
            #creo l'oggetto che verrà mandato alla tabella del DB durante il save
            data_to_mysql = User.objects.create(username=username, email=email, fullname=fullname, age=age, gender=gender, password=hashed_psw)
            #check se la password soddisfa i requisiti minimi
            if requirements_pass(not_hashed_psw):
                #procedimento di salvataggio dati nel DB
                form.save(data_to_mysql)
                return redirect('login')
            else:
                req_psw = True
                return render(request, "register.html", {'form': form, 'req_psw': req_psw})
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

####### logout function ########
def logout(request):
    return render(request, "index.html")

def recovery(request):
    return render(request, "recovery.html")
