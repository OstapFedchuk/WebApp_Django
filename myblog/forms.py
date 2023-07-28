from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


''' Questo file serve per la gestione dei form all'interno del WebApp.
    Potrebbe assomigliare al file models.py però models.py deve essere visto come 
    un file che serve per la creazione delle tabelle all'interno del nostro Database 
'''

GENDER_CHOICES = (
    ("", "Select Gender"),
    ("Male", "Male"),
    ("Female", "Female"),
    ("Unspecified", "Unspecified"),
)

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Enter Username", max_length=30)
    email = forms.EmailField(label="Enter Email", max_length=50)
    fullname = forms.CharField(label="Enter Fullname", max_length=100)
    age = forms.DateField(label="Enter your Age")
    gender = forms.ChoiceField(label="Select Gender", choices=GENDER_CHOICES)
    password1 = forms.CharField(label="Enter Password", max_length= 50, widget=forms.PasswordInput)
    password2 = forms.CharField(label="ConfirmPassword", max_length=50,  widget=forms.PasswordInput)

    '''
       Ho creato due unique key per non fare in modo tale che 
       username e email dipendano uno dall'altro(username+email)
       quindi adesso è (username/email)
    '''
    class Meta:
        model = User
        fields = ['username', 'email', 'fullname', 'age', 'gender', 'password1', 'password2']
