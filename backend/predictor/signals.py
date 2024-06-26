from django.db.models.signals import post_save
from django.dispatch import receiver

from predictor.models import CapturedWeatherData, WeatherData
from predictor.utils import create_weather_data


@receiver(post_save, sender=CapturedWeatherData)
def sync_weater_data(sender, instance, created, **kwargs):
    if not instance.weather_data:
        instance.weather_data = create_weather_data(instance.longitude, instance.latitude)
        instance.save()
