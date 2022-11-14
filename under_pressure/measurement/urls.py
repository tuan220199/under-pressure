from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("temperature", views.temperature, name="temperature"),
    path("humidity", views.humidity, name="humidity"),
    path("pressure", views.pressure, name="pressure"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]