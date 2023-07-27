from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("info", views.info, name="info"),
    path("gitstatus", views.gitstatus, name="gitstatus"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("", views.logout, name="logout"),
    path("recovery", views.recovery, name="recovery")
]