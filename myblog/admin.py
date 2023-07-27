from django.contrib import admin
from .models import User, Contact

# Register your models here.
#da la possibilità di modificare i modelli creati tramite admin user
admin.site.register(User)
admin.site.register(Contact)