from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

''' Questo file serve per la gestione dei form all'interno del WebApp.
    Potrebbe assomigliare al file models.py però models.py deve essere visto come 
    un file che serve per la creazione delle tabelle all'interno del nostro Database 
'''

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=50)
    fullname = forms.CharField(max_length=100)
    age = forms.CharField(max_length=20)
    gender = forms.CharField(max_length=10)
    password = forms.CharField(max_length= 50)

    '''
       Ho creato due unique key per non fare in modo tale che 
       username e email dipendano uno dall'altro(username+email)
       quindi adesso è (username/email)
    '''

    class Meta:
        model = User
        fields = ['username', 'email', 'fullname', 'age', 'gender', 'password']
