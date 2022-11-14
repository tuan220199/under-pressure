from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.login_view, name="login"),
    path("index", views.index, name="index"),
    path("temperature", views.temperature, name="temperature"),
    path("humidity", views.humidity, name="humidity"),
    path("pressure1", views.pressure1, name="pressure1"),
    path("pressure2", views.pressure2, name="pressure2"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]

urlpatterns += staticfiles_urlpatterns()