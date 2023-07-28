from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    fullname = models.CharField(max_length=100)
    age = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    password1 = models.CharField(max_length= 50)
    
    '''Ho creato due unique key per non fare in modo tale che 
       username e email dipendano uno dall'altro(username+email)
       quindi adesso è (username/email)
    '''
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email'], name='unique_email'
            ),
            models.UniqueConstraint(
                fields=['username'], name='unique_username'
            )
        ]


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)