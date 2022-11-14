from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from .models import User, Temperature, Humidity, Pressure1, Pressure2
from .models import User, Temperature, Humidity, Pressure1, Pressure2
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Temperature)
admin.site.register(Humidity)
admin.site.register(Pressure1)
admin.site.register(Pressure2)