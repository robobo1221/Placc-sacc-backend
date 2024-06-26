from django.contrib import admin
from .models import WeatherData, CapturedWeatherData

# Register your models here.

admin.site.register(WeatherData)

admin.site.register(CapturedWeatherData)