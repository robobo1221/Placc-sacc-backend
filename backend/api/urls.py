from django.urls import path, include
from .views import WeatherDataView, BuienRadarView, StickyWeatherPredictionView, ForecastStickyWeatherView, CapturedWeatherDataView

app_name = 'api'

urlpatterns = [
    path('weatherdata', WeatherDataView.as_view(), name='weatherdata'),
    path('buienradar', BuienRadarView.as_view(), name='buienradar'),
    path('stickyprediction', StickyWeatherPredictionView.as_view(), name='stickyprediction'),
    path('forecaststicky', ForecastStickyWeatherView.as_view(), name='forecaststicky'),
    path('capturedweatherdata', CapturedWeatherDataView.as_view(), name='capturedweatherdata'),
]