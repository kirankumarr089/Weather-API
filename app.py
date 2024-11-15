from flask import Flask, request, render_template
import requests
import datetime as dt

app = Flask(__name__)

API_key = '4f0bc35c0aead4c85b9e70526aaf9690'

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city'].capitalize()
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}'
        response = requests.get(url).json()
        
        if response.get('main'):
            temp_kelvin = response['main']['temp']
            temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
            feels_like_kelvin = response['main']['feels_like']
            feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
            humidity = response['main']['humidity']
            wind_speed = response['wind']['speed']
            description = response['weather'][0]['description']
            icon = response['weather'][0]['icon']
            sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
            sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
            
            weather_data = {
                'city': city,
                'temp_celsius': f"{temp_celsius:.2f}",
                'temp_fahrenheit': f"{temp_fahrenheit:.2f}",
                'feels_like_celsius': f"{feels_like_celsius:.2f}",
                'feels_like_fahrenheit': f"{feels_like_fahrenheit:.2f}",
                'humidity': humidity,
                'wind_speed': wind_speed,
                'description': description,
                'icon': icon,
                'sunrise_time': sunrise_time.strftime('%Y-%m-%d %H:%M:%S'),
                'sunset_time': sunset_time.strftime('%Y-%m-%d %H:%M:%S'),
            }
        else:
            weather_data = {'error': 'City not found'}
        
        return render_template('index.html', weather_data=weather_data)
    return render_template('index.html', weather_data=None)

if __name__ == '__main__':
    app.run(debug=True)
