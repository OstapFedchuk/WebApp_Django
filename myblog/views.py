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
                pass_db = UserData.objects.values_list('password', flat=True)
                print(pass_db)
                #controllo se le password corrispondano
                #if password_form == decode_pass: 
                if bcrypt.checkpw(password_form.encode('utf-8'), pass_db.encode('utf-8')):
                    #metto in sessione l'Utente
                    request.session['username'] = gen_user
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
    
            #controllo se l'email è già in uso
            if UserData.objects.filter(email=email).exists():
                error = True
                return render(request, "register.html", {"error": error, "form": form})   
                
            #check se la password soddisfa i requisiti minimi
            if requirements_pass(password1):
                #procedimento per heshare la password
                password_encode = password1.encode('utf-8')
                hashed_psw = bcrypt.hashpw(password_encode, bcrypt.gensalt())
                stored_password = hashed_psw.decode('utf-8')

                #creo l'oggetto che verrà mandato alla tabella del DB durante il save
                data_to_mysql = UserData.objects.create(username=username, email=email, fullname=fullname, age=age, gender=gender, password=stored_password)
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

####### Recovery Password function ########
def recovery(request):
    error = False

    if request.method == "POST":
        form_data = request.POST
        #Purtroppo recupera solamente il form senza i dati 
        form = RecoveryForm(form_data) 
        if form.is_valid():
            gen_user = form_data['gen_user']
            
            #Do la possibilità di recuperare la password consocendo username o email
            if UserData.objects.filter(username=gen_user).exists() or UserData.objects.filter(email=gen_user).exists():
                #genero la password temporanea senza encoddarla
                clear_psw = password_generator()
                #encoddo la password generata
                rec_psw = clear_psw.encode('utf-8')
                #hesho la password encoddata
                hashed_rec_psw = bcrypt.hashpw(rec_psw, bcrypt.gensalt())
                #recupero la password dal DB
                x = UserData.objects.all()[6]
                #settola nuova password generata
                x.password = hashed_rec_psw
                #salvo nel DB
                x.save()
                
                return render(request, 'recovery.html', {'rec_psw': clear_psw, 'form': form})
            #se l'utente non esiste allora torna un errore
            else:
                error = True
                return render(request, 'recovery.html', {'error': error, 'form': form})
    else:
        form = RecoveryForm()
        return render(request,  'recovery.html', {'form': form})

    return render(request, "recovery.html")
