from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager

# Create your models here.
class UserData(AbstractBaseUser):
    username = models.CharField(max_length=45, default="", primary_key=True)
    email = models.EmailField(max_length=45, default="")
    fullname = models.CharField(max_length=100, default="")
    age = models.CharField(max_length=20, default="")
    gender = models.CharField(max_length=20, default='')
    password = models.CharField(max_length= 500, default="")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

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
