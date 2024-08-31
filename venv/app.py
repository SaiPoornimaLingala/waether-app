from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
API_KEY = 'ede8cc89f59289c3aab71a3a07ad02f3'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    if request.method == 'POST':
        city = request.form['city']
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        weather_response = requests.get(weather_url)
        forecast_response = requests.get(forecast_url)
        if weather_response.status_code == 200 and forecast_response.status_code == 200:
            weather_data = weather_response.json()
            forecast_data = forecast_response.json()
        else:
            weather_data = None

    return render_template('index.html', weather_data=weather_data, forecast_data=forecast_data)

@app.route('/location')
def location_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    weather_response = requests.get(weather_url)
    if weather_response.status_code == 200:
        return jsonify(weather_response.json())
    else:
        return jsonify({'error': 'Unable to fetch weather data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
