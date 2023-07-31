from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, null=True, default='')
    email = models.EmailField(max_length=50, null=False, default='')
    fullname = models.CharField(max_length=100, null=True, default='')
    age = models.CharField(max_length=20, null=True, default='')
    gender = models.CharField(max_length=10, null=True, default='')
    password = models.CharField(max_length= 50, null=True, default='')

    class Meta:
        db_table = 'database_mysql'
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)