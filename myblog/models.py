from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    email = models.EmailField(max_length=50)
    fullname = models.CharField(max_length=100)
    age = models.DateField(max_length=20)
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length= 50)
    
    #Per fare in modo tale che ci siano due 'primary key' indipendenti
    #visto che due primary key non ci possono stare
    #oppure se sono due unique keys, saranno dipendenti un dall'altro
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email'], name='unique_email'
            )
        ]


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)