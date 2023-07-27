from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

''' Questo file serve per la gestione dei form all'interno del WebApp.
    Potrebbe assomigliare al file models.py però models.py deve essere visto come 
    un file che serve per la creazione delle tabelle all'interno del nostro Database 
'''

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, primary_key=True)
    email = forms.EmailField(max_length=50)
    fullname = forms.CharField(max_length=100)
    age = forms.DateField()
    gender = forms.CharField(max_length=10)
    password = forms.CharField(max_length= 50)

    #Per fare in modo tale che ci siano due 'primary key' indipendenti
    #visto che due primary key non ci possono stare
    #oppure se sono due unique keys, saranno dipendenti un dall'altro
    
    class Meta:
        constraints = [
            forms.UniqueConstraint(
                fields=['email'], name='unique_email'
            )
        ]
