from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserData(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, default="")
    email = models.EmailField(max_length=50, default="", unique=True)
    fullname = models.CharField(max_length=100, default="")
    age = models.CharField(max_length=20, default="")
    gender = models.CharField(max_length=20, default="")
    password = models.CharField(max_length= 500, default="")

    class Meta:
        db_table = 'myblog_user'
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]
    
    def __str__(self):
        return self.username


class Contact(models.Model):
    name = models.CharField(max_length=50, default='')
    email = models.EmailField(max_length=50, default='')
    subject = models.CharField(max_length=100, default='')
    message = models.TextField(max_length=2000, default='')

    class Meta:
        db_table = 'myblog_contact'
