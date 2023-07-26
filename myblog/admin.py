from django.contrib import admin
from .models import Signup, Contact

# Register your models here.
#da la possibilità di modificare i modelli creati tramite admin user
admin.site.register(Signup)
admin.site.register(Contact)