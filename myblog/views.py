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
    if 'username' in request.session:
       return render(request, 'index.html', {'global_username': request.session['username']})
    else:
        return render(request, 'index.html', {'global_username': "Guest"})

def about(request):
    if 'username' in request.session:
       return render(request, 'about.html', {'global_username': request.session['username']})
    else:
        return render(request, 'about.html', {'global_username': "Guest"})

####### contact function #######
def contact(request):
    #serve per mostrare il username vicino all'icona del user, se è loggato
    if 'username' in request.session:
        return render(request, 'index.html', {'global_username': request.session['username']})
    
    #Procedimento di salvataggio dei dati nel myblog_contact
    if request.method == 'POST':
        form_data = request.POST
        form = ContactForm(form_data)
        if form.is_valid():
            name = form_data['name']
            email = form_data['email']
            subject = form_data['subject']
            message = form_data['message']
            
            form.save()
            return redirect('index')
        
        #se l'utente non è loggato allora sarà Guest
        else:
            return render(request, 'index.html', {'global_username': "Guest"})
    else:
        form = ContactForm()
    return render(request, "contact.html", {'form': form})


def info(request):
    if 'username' in request.session:
       return render(request, 'info.html', {'global_username': request.session['username']})
    else:
        return render(request, 'info.html', {'global_username': "Guest"})

def gitstatus(request):
    return render(request, "gitstatus.html")

############## login function ###############
def login(request):
    error = False
    
    if request.method == 'POST':
        form_data = request.POST
        form = LoginForm(form_data) 
        if form.is_valid():
            gen_user =  form_data['gen_user']
            password_form = form_data['password']
            
            #controllo se username o email esistono(Se mi loggo con l'email verrò visualizzato il Username)
            if UserData.objects.filter(username=gen_user).exists() or UserData.objects.filter(email=gen_user).exists():
                query_set = UserData.objects.values_list('username', flat=True)
                pass_db = UserData.objects.values_list('password', flat=True)
                #query_set = UserData.objects.get(username=gen_user) #prendo tutta la riga dal DB coi dati
                #pass_db = query_set.first()['password'] #ricavo dalla riga la password
                decode_pass = pass_db.decode('utf-8') # la decodo
                
                #controllo se le password corrispondano
                if password_form == decode_pass: 
                    #metto in sessione l'Utente
                    request.session['username'] = query_set
                    return redirect('index')
            #Altrimenti, errore, credenziali sbagliati
            else:
                error = True
                return render(request, 'login.html', {'error': error})
    else:
        form = LoginForm()
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
            password2 = form_data['password2']

            #procedimento per heshare la password
            not_hashed_psw = password1
            password1 = password1.encode('utf-8')
            hashed_psw = bcrypt.hashpw(password1, bcrypt.gensalt())

            #controllo se l'email è già in uso
            if UserData.objects.filter(email=email).exists():
                error = True
                return render(request, "register.html", {"error": error, "form": form})   
                
            #check se la password soddisfa i requisiti minimi
            if requirements_pass(not_hashed_psw):
                #creo l'oggetto che verrà mandato alla tabella del DB durante il save
                data_to_mysql = UserData.objects.create(username=username, email=email, fullname=fullname, age=age, gender=gender, password=hashed_psw)
                #procedimento di salvataggio dati nel DB
                form.save(data_to_mysql)
                return redirect('login')
            #DA CAPIRE PERCHE SALVA LA PASSWORD e da il messaggio di errore
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
