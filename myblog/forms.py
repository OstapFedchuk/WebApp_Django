from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm


''' Questo file serve per la gestione dei form all'interno del WebApp.
    Potrebbe assomigliare al file forms.py però forms.py deve essere visto come 
    un file che serve per la creazione delle tabelle all'interno del nostro Database 
'''

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Unspecified", "Unspecified"),
)

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Enter Username", max_length=30, required=True)
    email = forms.EmailField(label="Enter Email", max_length=50, required=True)
    fullname = forms.CharField(label="Enter Fullname", max_length=100, required=True)
    age = forms.DateField(label="Enter your BirthDay", widget=forms.DateInput(attrs=dict(type='date')), required=True)
    gender = forms.ChoiceField(label="Select Gender", choices=GENDER_CHOICES, required=True)
    password1 = forms.CharField(label="Enter Password", max_length= 50, widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="ConfirmPassword", max_length=50,  widget=forms.PasswordInput, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'fullname', 'age', 'gender', 'password1', 'password2']


class LoginForm(forms.Form):
    gen_user = forms.CharField(label="Enter Username or Email", max_length=50, required=True)
    password = forms.CharField(label="Enter Password", max_length=50, widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['gen_user', 'password']

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=50, required=True)
    email = forms.EmailField(label='Your Email',max_length=50, required=True)
    subject = forms.CharField(label='Subject',max_length=100, required=True)
    message = forms.CharField(label='The Message',widget=forms.Textarea, required=True)
