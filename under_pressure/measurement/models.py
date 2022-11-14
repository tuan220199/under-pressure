from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    # already have username, email and password
    pass

class Temperature(models.Model):
    value = models.FloatField()
    time = models.CharField(max_length=64)
    risk_PU = models.BooleanField(default=False)
    user_temperature = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_temperature")

    def __str__(self):
        return f"{self.value}"

class Humidity(models.Model):
    value = models.FloatField()
    time = models.CharField(max_length=64)
    risk_PU = models.BooleanField(default=False)
    user_humidity = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_humidity")

    def __str__(self):
        return f"{self.value}"

class Pressure1(models.Model):
    pressure_value = models.FloatField()
    Tp_value = models.FloatField()
    time = models.CharField(max_length=64)
    risk_PU = models.BooleanField(default=False)
    user_pressure1 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_pressure1")

    def __str__(self):
        return f"{self.pressure_value} in {self.Tp_value} minutes"

class Pressure2(models.Model):
    pressure_value = models.FloatField()
    Tp_value = models.FloatField()
    time = models.CharField(max_length=64)
    risk_PU = models.BooleanField(default=False)
    user_pressure2 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_pressure2")

    def __str__(self):
        return f"{self.pressure_value} in {self.Tp_value} minutes"
