from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, null=True, default='')
    email = models.EmailField(max_length=50, null=False, default='', primary_key=True)
    fullname = models.CharField(max_length=100, null=True, default='')
    age = models.CharField(max_length=20, null=True, default='')
    gender = models.CharField(max_length=10, null=True, default='')
    password = models.CharField(max_length= 50, null=True, default='')
    
    '''Ho creato due unique key per non fare in modo tale che 
       username e email dipendano uno dall'altro(username+email)
       quindi adesso è (username/email)
    '''



class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)