from django.db import models

# Create your models here.
class Signup(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    fullname = models.CharField(max_length=100)
    age = models.DateField(max_length=20)
    gender = models.CharField(max_length=10)
    
    #Assign multiple Primary Key
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user'
            )
        ]


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)