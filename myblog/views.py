''' Creo le mie funzoni per i miei template'''

from django.shortcuts import render, HttpResponse
from .models import Signup, Contact

# Create your views here.
def index(request):
    global_username = "Giovanni"
    return render(request, "index.html", {"global_username": global_username})
