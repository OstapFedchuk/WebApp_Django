''' Creo le mie funzoni per i miei template'''

from django.shortcuts import render, redirect
from django.views.generic import CreateView
import bcrypt
from .models import User, Contact
from .functions import *

class CreatePerson(CreateView):
    model = UserRegisterForm
    template_name = 'register.html'
    fields = ['username', 'email', 'fullname', 'age', 'gender', 'password']

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
    error = False
    req_psw = False

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            not_hashed_psw = password1
            #procedimento per heshare la password
            password1 = password1.encode('utf-8')
            hashed_psw = bcrypt.hashpw(password1, bcrypt.gensalt())

            if check_user_exist(username) or check_email_exist(email):
                error = True
                return render(request, "register.html", {'error': error})
            
            if form.password1 == form.password2:
                if requirements_pass(not_hashed_psw):
                    register_user_to_db(username,email,fullname,age,gender,hashed_psw)
                    
                    form.save()

                    username = form.cleaned_data.get('username')
                    email = form.cleaned_data.get('email')
                    fullname = form.cleaned_data.get('fullname')
                    age = form.cleaned_data.get('age')
                    gender = form.cleaned_data.get('gender')
                    password1 = form.cleaned_data.get('password1')
                    password2 = form.cleaned_data.get('password2')

                    messages.success(request, f'Your account has been creted')
                    return redirect('login')
                else:
                    req_psw = True
                    return render(request, "register.html", {'req_psw': req_psw})
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def logout(request):
    return render(request, "index.html")

def recovery(request):
    return render(request, "recovery.html")
