from django.contrib import admin
from .models import *

# Register your models here.
#da la possibilità di modificare i modelli creati tramite admin user
admin.site.register(UserData)
admin.site.register(Contact)