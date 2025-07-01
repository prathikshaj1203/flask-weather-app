from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# ✅ Load the .env file
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        api_key = os.getenv('WEATHER_API_KEY')  # Pull from .env

        if not api_key:
            weather_data = {'error': '🔐 API key not found in .env file.'}
        else:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'wind': data['wind']['speed'],
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon']
                }

            except requests.exceptions.Timeout:
                weather_data = {'error': '⏱️ Request timed out. Try again.'}
            except requests.exceptions.HTTPError:
                weather_data = {'error': '❌ City not found or invalid response.'}
            except requests.exceptions.RequestException as e:
                weather_data = {'error': f'⚠️ Error: {e}'}

    return render_template('index.html', wd=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
