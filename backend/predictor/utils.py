from predictor.models import WeatherData
from predictor.models import CapturedWeatherData
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier


from sklearn.svm import SVC
import numpy as np
import math

def get_weather_data(sticky = None):
    weather_data = WeatherData.objects.all()

    if sticky is not None:
        weather_data = weather_data.filter(capturedweatherdata__sticky_sack=sticky).order_by('-capturedweatherdata__captured_at')

    if not weather_data.exists():
        return None

    return weather_data.values()

def calculate_sticky_probability(temp: float, humidity: float, wind_speed: float, precipitation: float, captured_data = None):
    if captured_data is None:
        captured_data = CapturedWeatherData.objects.all()
        if not captured_data.exists():
            return 0.0

    X = []
    y = []
    for data in captured_data:
        if not data or not data.weather_data:
            continue

        X.append([data.weather_data.temperature,
                  data.weather_data.humidity,
                  data.weather_data.wind_speed,
                  data.weather_data.precipitation])
        y.append(data.sticky_sack)
    
    # Convert lists to numpy arrays
    X = np.array(X)
    y = np.array(y)
    
    # Train the logistic regression model
    model = LogisticRegression(random_state=0, max_iter=10000)
    model.fit(X, y)
    
    # Predict the probability of sticky weather
    input_data = np.array([[temp, humidity, wind_speed, precipitation]])
    probability = model.predict_proba(input_data)[:, 1]
    
    return probability

def get_buienradar_data(lat: float, lon: float):
    from buienradar.buienradar import (get_data, parse_data)
    from buienradar.constants import (CONTENT, RAINCONTENT, SUCCESS)

    result = get_data(latitude=lat, longitude=lon)
    if result.get(SUCCESS):
        data = result[CONTENT]
        rain_data = result[RAINCONTENT]

        parsed_data = parse_data(data, rain_data, lat, lon)
        return parsed_data['data']

    raise Exception('Failed to get data from Buienradar')

def create_weather_data(lon: float, lat: float, buienradar_data: dict = None):
    if not buienradar_data:
        data = get_buienradar_data(lat=lat, lon=lon)
    else:
        data = buienradar_data

    if data:
        temp = data['temperature']
        humidity = data['humidity']
        wind_speed = data['windspeed']
        precipitation = data['precipitation']

        if temp is None:
            temp = 16.0

        if wind_speed is None:
            wind_speed = 0

        if precipitation is None:
            precipitation = 0

        if humidity is None:
            humidity = 25

        weather_data = WeatherData.objects.create(temperature=temp, humidity=humidity, wind_speed=wind_speed, precipitation=precipitation)
        return weather_data

    return None

def predict_sticky_weather(lon: float, lat: float):
    data = get_buienradar_data(lat=lat, lon=lon)

    if data:        
        temp = data['temperature']
        wind_speed = data['windspeed']
        precipitation = data['precipitation']
        humidity = data['humidity']

        if temp is None:
            temp = 16.0

        if wind_speed is None:
            wind_speed = 0

        if precipitation is None:
            precipitation = 0

        if humidity is None:
            humidity = 25

        probability = calculate_sticky_probability(temp, humidity, wind_speed, precipitation)
        return probability

    return None

def forecast_sticky_weather(lon: float, lat: float):
    data = get_buienradar_data(lat=lat, lon=lon)

    forecast_list = []

    captured_data = CapturedWeatherData.objects.all()
    if not captured_data.exists():
        return forecast_list

    if data:
        for forecast in data['forecast']:
            temp = forecast['maxtemp']
            wind_speed = forecast['windspeed']
            precipitation = forecast['rain'] * 0.1
            humidity = estimate_humidity(temp, forecast['sunchance'], wind_speed, forecast['rainchance'])

            probability = calculate_sticky_probability(temp, humidity, wind_speed, precipitation, captured_data)
            forecast_list.append({
                "datetime": str(forecast['datetime']),
                "probability": probability})
            
    nearest_station = data['stationname']
        
    return [nearest_station, forecast_list]

def estimate_dew_point(temp_c, rh):
    a = 17.27
    b = 237.7
    alpha = (a * temp_c) / (b + temp_c) + math.log(rh / 100.0)
    dew_point = (b * alpha) / (a - alpha)
    return dew_point

def estimate_humidity(temp_c, sunchance, windspeed, rainchance):
    initial_rh = 50
    dew_point = estimate_dew_point(temp_c, initial_rh)
    
    # Empirical coefficients
    k = 0.5
    m = 0.1
    n = 0.5
    
    rh = 100 - 0.5 * (temp_c - dew_point) - k * sunchance - m * windspeed + n * rainchance
    rh = max(0, min(rh, 100))  # Ensure RH is within 0-100%
    
    return rh