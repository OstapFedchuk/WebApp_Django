from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, default="")
    email = models.EmailField(max_length=50, default="")
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
        return self.username, self.email, self.password


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)