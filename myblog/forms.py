from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from DjangoWebApp.settings import DB_table


''' Questo file serve per la gestione dei form all'interno del WebApp.
    Potrebbe assomigliare al file models.py però models.py deve essere visto come 
    un file che serve per la creazione delle tabelle all'interno del nostro Database 
'''

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Unspecified", "Unspecified"),
)

class UserRegisterForm(forms.Form):
    username = forms.CharField(label="Enter Username", max_length=30)
    email = forms.EmailField(label="Enter Email", max_length=50)
    fullname = forms.CharField(label="Enter Fullname", max_length=100)
    age = forms.DateField(label="Enter your BirthDay", widget=forms.DateInput(attrs=dict(type='date')))
    gender = forms.ChoiceField(label="Select Gender", choices=GENDER_CHOICES)
    password1 = forms.CharField(label="Enter Password", max_length= 50, widget=forms.PasswordInput)
    password2 = forms.CharField(label="ConfirmPassword", max_length=50,  widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'fullname', 'age', 'gender', 'password1', 'password2']

    def save(self, commit=True):
        #user = super().save(commit=False) #hash the password
        user = User(username=self.username, email=self.email, fullname=self.fullname, age=self.age, gender=self.gender, password=self.password1)
        user.save(DB_table)
        return user

class LoginForm(forms.Form):
    gen_user = forms.CharField(label="Enter Username or Email", max_length=50)
    password = forms.CharField(label="Enter Password", max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['gen_user', 'password']
