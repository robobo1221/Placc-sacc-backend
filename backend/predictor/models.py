from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class WeatherData(models.Model):
    temperature = models.FloatField(_('Temperature'), null=True, blank=True)
    humidity = models.FloatField(_('Humidity'), null=True, blank=True)
    wind_speed = models.FloatField(_('Wind Speed'), null=True, blank=True)
    precipitation = models.FloatField(_('Precipitation'), null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk} {self.temperature}°C, {self.humidity}%, {self.wind_speed}m/s, {self.precipitation}mm'

class CapturedWeatherData(models.Model):
    weather_data = models.OneToOneField(WeatherData, on_delete=models.CASCADE, null=True, blank=True)
    sticky_sack = models.BooleanField(_('Sticky Sack'), default=False)

    longitude = models.FloatField(_('Longitude'), null=True, blank=True)
    latitude = models.FloatField(_('Latitude'), null=True, blank=True)

    captured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.weather_data}'