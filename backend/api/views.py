from rest_framework.views import APIView
from rest_framework.response import Response
from predictor.models import CapturedWeatherData

from predictor.utils import get_weather_data, predict_sticky_weather, forecast_sticky_weather
from .util import get_boolean_query_item

from buienradar.buienradar import (get_data, parse_data)
from buienradar.constants import (CONTENT, RAINCONTENT, SUCCESS)

class WeatherDataView(APIView):
    def get(self, request, *args, **kwargs):
        sticky = get_boolean_query_item(request, 'sticky')

        weather_data = get_weather_data(sticky=sticky)

        if not weather_data:
            return Response({'error': 'No weather data found.'}, status=404)

        return Response(weather_data.values())
    
class BuienRadarView(APIView):
    def get(self, request, *args, **kwargs):
        lat = request.query_params.get('lat', None)
        lon = request.query_params.get('lon', None)

        if lat is None or lon is None:
            return Response({'error': 'Latitude and longitude are required.'}, status=400)
        
        lat = float(lat)
        lon = float(lon)
        
        result = get_data(latitude=lat, longitude=lon)
        if result.get(SUCCESS):
            data = result[CONTENT]
            rain_data = result[RAINCONTENT]

            parsed_data = parse_data(data, rain_data, lat, lon)
            return Response(parsed_data)
        
        return Response({'error': 'Failed to get data from Buienradar.'}, status=500)
    
class StickyWeatherPredictionView(APIView):
    def get(self, request, *args, **kwargs):
        lat = request.query_params.get('lat', None)
        lon = request.query_params.get('lon', None)

        if lat is None or lon is None:
            return Response({'error': 'Latitude and longitude are required.'}, status=400)
        
        lat = float(lat)
        lon = float(lon)
        
        result = predict_sticky_weather(lat, lon)
        if result is None:
            return Response({'error': 'Failed to predict sticky weather.'}, status=500)
        
        return Response({'probability': result})

class ForecastStickyWeatherView(APIView):
    def get(self, request, *args, **kwargs):
        lat = request.query_params.get('lat', None)
        lon = request.query_params.get('lon', None)

        if lat is None or lon is None:
            return Response({'error': 'Latitude and longitude are required.'}, status=400)
        
        lat = float(lat)
        lon = float(lon)
        
        result = forecast_sticky_weather(lat, lon)
        if not result:
            return Response({'error': 'Failed to forecast sticky weather.'}, status=500)
        
        return Response({
            'nearest_station': result[0],
            'forecast': result[1],
        })
    
class CapturedWeatherDataView(APIView):
    def post(self, request, *args, **kwargs):
        lat = request.data.get('lat', None)
        lon = request.data.get('lon', None)
        sticky = request.data.get('sticky', True)

        if lat is None or lon is None:
            return Response({'error': 'Latitude and longitude are required.'}, status=400)
        
        lat = float(lat)
        lon = float(lon)
        
        weather_data = CapturedWeatherData.objects.create(longitude=lon, latitude=lat, sticky_sack=sticky)
        
        if not weather_data or not weather_data.weather_data:
            return Response({'error': 'Failed to create weather data.'}, status=500)
        
        return Response({'id': weather_data.id})